
# The number of frames per video in which detect the noun
# (to be removed when parameters and models are improved)
# This number is low, because it takes a long time to run
# the detection over an image on my CPU, and sometimes
# the videos don't have the desired object in them. When
# they don't, I add the video_id to the blacklist in the
# video_id_fetcher. If I were using only videos not on the
# blacklist, I would increase this number.
N_FRAMES = 7

# The number of frames skipped at the beggining of each video,
# Because they're usually title screens
NUM_FIRST_FRAMES_SKIPPED = 1

# Non-maximum suppression: Greedily select high-scoring detections and
# skip detections that are significantly covered by a previously
# selected detection. The defaut is 0.3
NON_MAXIMAL_SUPPRESSION_OVERLAP_THRESHOLD = 0.1

# The positive prediction score divided by the sum of the positive
# and negative prediction scores must be
# greater than this number in order to be considered a positive prediction.
# When I trained on a high ratio of negative:positive classes on the NIN
# model, the results were totally skewed to the negative class such that
# all positive scores were 0. So to help reduce the false positive rate,
# I increase this value.
POSITIVE_PREDICTION_SCORE_THRESHOLD = 0.7

# TODO This constant is out-of-date.
# If the noun is in this percentage of the highest predictions
# of ImageNet classes, annotate the image frame with the
# noun, the prediction score, and the bounding box.
TOP_PERCENTAGE = 0.005

