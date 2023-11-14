from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models, layers
import os

# 생성자
def build_generator(z_dim):
    model = models.Sequential()
    model.add(layers.Dense(256, input_dim=z_dim))
    model.add(layers.LeakyReLU(alpha=0.01))
    model.add(layers.BatchNormalization(momentum=0.8))

    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(alpha=0.01))
    model.add(layers.BatchNormalization(momentum=0.8))

    # 출력 크기를 (128, 128, 1)로 설정
    model.add(layers.Dense(1024 * 1024 * 1, activation='tanh'))
    model.add(layers.Reshape((1024, 1024, 1)))
    return model


# 판별자
def build_discriminator(img_shape):
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=img_shape))

    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(alpha=0.01))
    model.add(layers.Dropout(0.3))

    model.add(layers.Dense(256))
    model.add(layers.LeakyReLU(alpha=0.01))
    model.add(layers.Dropout(0.3))

    model.add(layers.Dense(128))
    model.add(layers.LeakyReLU(alpha=0.01))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model


# GAN
def build_gan(generator, discriminator):
    model = models.Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# 데이터 준비
# img = image.load_img('./resize_sheets/', color_mode='grayscale')
# img_array = image.img_to_array(img)
# print(img_array.shape)

# 파라미터
OUT_DIR ='./GAN_OUT'
img_shape = (1024, 1024, 1)
epochs = 100000
batch_size = 128
noise = 100
noise_dim = 100
sample_interval = 100


MY_NUMBER = 1

discriminator = build_discriminator(img_shape)
discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
discriminator.trainable = False  # GAN 학습 중 판별자의 가중치는 고정

generator = build_generator(100)
gan = build_gan(generator, discriminator)
gan.compile(loss='binary_crossentropy', optimizer='adam')


def load_image(file_path):
    """ png를 텐서로 바꿔주는 함수 """
    image = tf.io.read_file(file_path)
    image = tf.io.decode_png(image, channels=1) # PNG를 디코딩
    image = tf.image.convert_image_dtype(image, tf.float32)  # [0, 1] 범위로 변환
    return image

def load_dataset(directory, batch_size):
    # 파일 경로 리스트 생성
    file_paths = [os.path.join(directory, file_name) for file_name in os.listdir(directory)]
    dataset = tf.data.Dataset.from_tensor_slices(file_paths)
    dataset = dataset.map(load_image)
    dataset = dataset.batch(batch_size)
    return dataset

preprocess01_rgba_to_grayScale.py
preprocess02_resize_img.py
# 데이터셋 로드
dataset = load_dataset('./resize_sheets/', batch_size=32)

def generate_and_save_images(model, epoch, test_input, save_dir):
    """ 생성자로부터 이미지를 생성하고 저장하는 함수 """
    predictions = model(test_input, training=False)

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i+1)
        plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        plt.axis('off')

    # 이미지 저장
    save_path = os.path.join(save_dir, f'image_at_epoch_{epoch:04d}.png')
    plt.savefig(save_path)
    plt.close()

# 잡음 벡터 생성
seed = tf.random.normal([16, noise_dim])

half_batch = int(batch_size / 2)
for epoch in range(epochs):
    # 진짜 이미지와 가짜 이미지의 배치를 가져옴
    real_images = next(iter(dataset)).numpy()
    real_images = real_images[:half_batch]  # 진짜 이미지의 크기를 half_batch로 조정
    real_labels = np.ones((half_batch, 1))

    # 잡음을 생성하여 가짜 이미지를 생성
    noise = np.random.normal(0, 1, (half_batch, noise_dim))
    fake_images = generator.predict(noise)
    fake_labels = np.zeros((half_batch, 1))

    # 진짜 이미지와 가짜 이미지의 배치를 학습
    d_loss_real = discriminator.train_on_batch(real_images, real_labels)
    d_loss_fake = discriminator.train_on_batch(fake_images, fake_labels)
    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

    # 잡음을 생성
    noise = np.random.normal(0, 1, (batch_size, noise_dim))

    # 생성자가 가짜 이미지를 만들고, 판별자를 속이도록 학습
    valid_y = np.ones((batch_size, 1))
    g_loss = gan.train_on_batch(noise, valid_y)

    # 에폭마다 진행 상황을 출력
    if epoch % sample_interval == 0:
        print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100 * d_loss[1]}] [G loss: {g_loss}]")
    # 100에폭마다 생성한 이미지를 저장
    if (epoch + 1) % 100 == 0:
        generate_and_save_images(generator, epoch + 1, seed, OUT_DIR)

    generator.save('./models/generator_1.h5')
