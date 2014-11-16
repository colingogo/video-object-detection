'''
Positive training images must exist in `data/imagenet/<wnid>/train/positive`

To generate these training images, run:
  python imagenet_image_fetcher.py --wnid=<wnid>
If you want:
  Either:
    a.) manually filter these images using `filter_positive_images.py`
    or
    b.) run `draw_bounding_boxes.py` followed with `bounded_box_cropper.py`,
  in case b, the images will be stored in
  `cropped` rather than `all`
Else:
  rename the `all` dir to `train/positive`

Then run this script.
'''

import gflags
from gflags import FLAGS
from flags import set_gflags

# This default wnid is for eggs
gflags.DEFINE_string('wnid', 'n07840804',
                     'The wordnet id of the noun in the positive images')

# This ratio default is used in
# http://people.csail.mit.edu/torralba/publications/datasets_cvpr11.pdf
# "For detection the number of negatives is naturally much larger and
# more diverse".
gflags.DEFINE_integer('negative_to_positive_train_ratio', 10, '')
# 2000 ideally, but I'm going for speed right now:
gflags.DEFINE_integer('negative_to_positive_test_ratio', 100, '')
# The above ratio default is similar to the number of bounding boxes detected
# via selective search for each image.

# This ratio default is high because I don't use this test
# (validation, really) set to train hyperparamaters, just to judge accuracy.
# Otherwise I'd use 6, as in the
# Maxout Networks paper: arxiv.org/pdf/1302.4389v4.pdf
gflags.DEFINE_integer('train_to_test_ratio', 20, '')

import sys
import glob
from os.path import dirname, abspath, join, listdir, exists

from imagenet_image_fetcher import get_images, download_bounding_boxes

ROOT = dirname(abspath(__file__))


def create_train_and_test_splits()
  '''
  Directories created in data/imagenet/<wnid>/images:
    train/positive
    train/negative
    test/positive
    test/negative

  This function does not preprocess the images. I let caffe resize the
  images to 256x256.

  caffe needs to know the image categories. It does so by reading a
  text file for each the train set and the test set, of this format:

  /home/my_test_dir/picture-foo.jpg 0
  /home/my_test_dir/picture-foo1.jpg 1

  where picture-foo belongs to category 0 and picture-foo1 belongs
  to category 1 (I call category 1 the positive category).

  These two files are created in data/imagenet/<wnid>/image-categories:
    train.txt
    test.txt
  '''
  wnid_dir = join(ROOT, 'data/imagenet', FLAGS.wnid)
  images_dir = join(wnid_dir, 'images')
  positive_images_train_dir = join(images_dir, 'train/positive')
  negative_images_train_dir = join(images_dir, 'train/negative')
  positive_images_test_dir = join(images_dir, 'test/positive')
  negative_images_test_dir = join(images_dir, 'test/negative')

  if not exists(positive_images_train_dir):
    print 'The positive_images_train_dir must be populated with images'
    sys.exit(1)

  system('mkdir -p ', negative_images_train_dir)
  system('mkdir -p ', positive_images_test_dir)
  system('mkdir -p ', negative_images_test_dir)

  cropped_dir = join(images_dir, 'cropped')
  if exists(cropped_dir):
    all_positive_images_dir = cropped_dir
  else:
    all_positive_images_dir = join(images_dir, 'all')

  num_positive_images = \
    len(glob.glob(all_positive_images_dir, '*.[Jj][Pp][Gg]'))

  num_positive_test_images = \
    int(num_positive_images / (1 + FLAGS.train_to_test_ratio))

  num_positive_train_images = num_positive_images - num_positive_test_images

  num_negative_train_images = \
    FLAGS.negative_to_positive_train_ratio * num_positive_train_images

  num_negative_test_images = \
    num_positive_test_images * FLAGS.negative_to_positive_test_ratio

  num_moved = 0
  for name in listdir(all_positive_images_dir):
    system('mv ' + join(all_positive_images_dir, name) + ' ' \
           positive_images_train_dir)
    num_moved += 1
    if num_moved == num_positive_train_images:
      break

  for name in listdir(all_positive_images_dir):
    system('mv ' + join(all_positive_images_dir, name) + ' ' \
           positive_images_test_dir)


  get_negative_images(FLAGS.wnid, num_negative_train_images,
                      negative_images_train_dir)
  get_negative_images(FLAGS.wnid, num_negative_test_images,
                      negative_images_test_dir)

  create_category_files('train')
  create_category_files('test')

def create_category_files(stage):
  '''
  `stage` is either 'train' or 'test'
  '''
  wnid_dir = join(ROOT, 'data/imagenet', FLAGS.wnid)
  positive_dir = join(wnid_dir, stage, 'positive')
  negative_dir = join(wnid_dir, stage, 'negative')
  with open(join(wnid_dir, 'image-categories/' + stage + '.txt'), 'w') as f:
    for name in listdir(positive_dir):
      f.write(join(positive_dir, name) + ' 1\n')
    for name in listdir(negative_dir):
      f.write(join(negative_dir, name) + ' 0\n')

if __name__ == '__main__':
  set_gflags()
  create_train_and_test_splits()


