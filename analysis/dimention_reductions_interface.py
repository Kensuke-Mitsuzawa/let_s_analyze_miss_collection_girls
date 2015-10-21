import dimension_reduction.picture_reduction as p_d
import codecs
import json

__author__ = 'kensuke-mi'


def generate_girls_position():
    PATH_TO_PICS_DIR = '../extracted/miss_collection/gray'
    PATH_TO_SAVE_PICKLE = './dimension_reduction/data_directory/miss_picture_matrix_obj.pickle'
    PATH_TO_INPUT_JSON = '../extracted/miss_collection/miss_member.json'
    path_to_pic_tsne_result = '../visualization/data_for_visual/miss_pics_tsne_obj.json'

    position_map_picture_tsne = p_d.picture_reduction_normal_tsne(PATH_TO_PICS_DIR, PATH_TO_INPUT_JSON, PATH_TO_SAVE_PICKLE)
    with codecs.open(path_to_pic_tsne_result, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_tsne, indent=4, ensure_ascii=False))


def generate_boys_position():
    PATH_TO_PICS_DIR = '../extracted/mr_collection/gray'
    PATH_TO_SAVE_PICKLE = './dimension_reduction/data_directory/mr_picture_matrix_obj.pickle'
    PATH_TO_INPUT_JSON = '../extracted/mr_collection/miss_member.json'
    path_to_pic_tsne_result = '../visualization/data_for_visual/mr_pics_tsne_obj.json'

    position_map_picture_tsne = p_d.picture_reduction_normal_tsne(PATH_TO_PICS_DIR, PATH_TO_INPUT_JSON, PATH_TO_SAVE_PICKLE)
    with codecs.open(path_to_pic_tsne_result, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_tsne, indent=4, ensure_ascii=False))


def generate_girls_position_deepNN():

    PATH_TO_INPUT_JSON = '../extracted/miss_collection/miss_member.json'
    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE = 'deep_learning/intermediate_files_pylearn2/toy_train/'
    PATH_TO_DEEPNN_TRAINED = 'deep_learning/intermediate_files_pylearn2/toy_train/rbm.pickle/dbm.pkl'
    PROJECT_NAME = 'toy_train'
    PATH_TO_SAVE_DEEP_NN_RESULT = '../visualization/data_for_visual/miss_pics_deepNN_obj.json'

    vector_numbers_index = [30, 46, 65]

    position_map_picture_deepNN = p_d.prepare_picture_matrix_with_deepNN_features(PATH_TO_INPUT_JSON,
                                                    PATH_TO_DEEPNN_TRAINED,
                                                    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE,
                                                    PROJECT_NAME,
                                                    vector_numbers_index)
    with codecs.open(PATH_TO_SAVE_DEEP_NN_RESULT, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_deepNN, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    #generate_girls_position()
    #generate_boys_position()
    generate_girls_position_deepNN()


