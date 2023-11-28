from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from magenta.models.onsets_frames_transcription import audio_label_data_utils
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import data
from magenta.models.onsets_frames_transcription import infer_util
from magenta.models.onsets_frames_transcription import train_util

from note_seq import midi_io
from note_seq.protobuf import music_pb2
import six
import tensorflow.compat.v1 as tf

from tqdm import tqdm
import os

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('config', 'onsets_frames',
                           'Name of the config to use.')
tf.app.flags.DEFINE_string('model_dir', None,
                           'Path to look for acoustic checkpoints.')
tf.app.flags.DEFINE_string(
    'checkpoint_path', None,
    'Filename of the checkpoint to use. If not specified, will use the latest '
    'checkpoint')
tf.app.flags.DEFINE_string(
    'hparams',
    '',
    'A comma-separated list of `name=value` hyperparameter values.')
tf.app.flags.DEFINE_boolean(
    'load_audio_with_librosa', False,
    'Whether to use librosa for sampling audio (required for 24-bit audio)')
tf.app.flags.DEFINE_string(
    'transcribed_file_suffix', '',
    'Optional suffix to add to transcribed files.')

def create_example(filename, sample_rate, load_audio_with_librosa):
  """Processes an audio file into an Example proto."""
  wav_data = tf.gfile.Open(filename, 'rb').read()
  example_list = list(
      audio_label_data_utils.process_record(
          wav_data=wav_data,
          sample_rate=sample_rate,
          ns=music_pb2.NoteSequence(),
          # decode to handle filenames with extended characters.
          example_id=six.ensure_text(filename, 'utf-8'),
          min_length=0,
          max_length=-1,
          allow_empty_notesequence=True,
          load_audio_with_librosa=load_audio_with_librosa))
  assert len(example_list) == 1
  return example_list[0].SerializeToString()

def run(argv, config_map, data_fn):
  """Create transcriptions."""
  config = config_map[FLAGS.config]
  hparams = config.hparams
  hparams.parse(FLAGS.hparams)
  hparams.batch_size = 1
  hparams.truncated_length_secs = 0

  with tf.Graph().as_default():
    examples = tf.placeholder(tf.string, [None])

    dataset = data_fn(
        examples=examples,
        preprocess_examples=True,
        params=hparams,
        is_training=False,
        shuffle_examples=False,
        skip_n_initial_records=0)

    estimator = train_util.create_estimator(config.model_fn,
                                            os.path.expanduser(FLAGS.model_dir),
                                            hparams)

    iterator = tf.data.make_initializable_iterator(dataset)
    next_record = iterator.get_next()

    with tf.Session() as sess:
      sess.run([
          tf.initializers.global_variables(),
          tf.initializers.local_variables()
      ])

      for filename in argv:
        # tf.logging.info('Starting transcription for %s...', filename)

        # The reason we bounce between two Dataset objects is so we can use
        # the data processing functionality in data.py without having to
        # construct all the Example protos in memory ahead of time or create
        # a temporary tfrecord file.
        # tf.logging.info('Processing file...')
        sess.run(iterator.initializer,
                 {examples: [
                     create_example(filename, hparams.sample_rate,
                                    FLAGS.load_audio_with_librosa)]})

        def transcription_data(params):
          del params
          return tf.data.Dataset.from_tensors(sess.run(next_record))
        input_fn = infer_util.labels_to_features_wrapper(transcription_data)

        # tf.logging.info('Running inference...')
        checkpoint_path = None
        if FLAGS.checkpoint_path:
          checkpoint_path = os.path.expanduser(FLAGS.checkpoint_path)
        prediction_list = list(
            estimator.predict(
                input_fn,
                checkpoint_path=checkpoint_path,
                yield_single_examples=False))
        assert len(prediction_list) == 1

        sequence_prediction = music_pb2.NoteSequence.FromString(
            prediction_list[0]['sequence_predictions'][0])

        midi_path = 'midi/'
        if not os.path.isdir(midi_path):
            os.mkdir(midi_path)

        wav_path = filename.split('\\\\')
        idx = wav_path[-1].find('.wav')

        midi_path += wav_path[-1][:idx]
        midi_filename = midi_path + '.midi'

        midi_io.sequence_proto_to_midi_file(sequence_prediction, midi_filename)

        tf.logging.info('Transcription written to %s.', midi_filename)

def wav_to_midi(filename):
    FLAGS.config = 'onsets_frames'
    FLAGS.model_dir = './models/maestro'

    wav_path = 'uploads\\\\'+filename
    argv = [wav_path]

    run(argv, config_map=configs.CONFIG_MAP, data_fn=data.provide_batch)

def midi_to_sheet():
    pass

filename = 'arpeggio-01-36024.wav'
wav_to_midi(filename)

