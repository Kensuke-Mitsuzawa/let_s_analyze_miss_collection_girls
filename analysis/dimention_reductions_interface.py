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
    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE = 'deep_learning/pylearn2_intermediate_files/girls_face_dmb'
    PATH_TO_DEEPNN_TRAINED = 'deep_learning/pylearn2_intermediate_files/girls_face_dmb/rbm.pickle/dbm.pkl'
    PROJECT_NAME = 'girls_face_dmb'
    PATH_TO_SAVE_DEEP_NN_RESULT = '../visualization/data_for_visual/miss_pics_deepNN_obj.json'

    # [-1] indicates to use all features
    vector_numbers_index = [-1]

    position_map_picture_deepNN = p_d.prepare_picture_matrix_with_deepNN_features(PATH_TO_INPUT_JSON,
                                                    PATH_TO_DEEPNN_TRAINED,
                                                    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE,
                                                    PROJECT_NAME,
                                                    vector_numbers_index,reduction_mode='t-sne')
    with codecs.open(PATH_TO_SAVE_DEEP_NN_RESULT, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_deepNN, indent=4, ensure_ascii=False))

    PATH_TO_SAVE_DEEP_NN_RESULT = '../visualization/data_for_visual/miss_pics_deepNN_pca_obj.json'
    position_map_picture_deepNN_pca = p_d.prepare_picture_matrix_with_deepNN_features(PATH_TO_INPUT_JSON,
                                                    PATH_TO_DEEPNN_TRAINED,
                                                    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE,
                                                    PROJECT_NAME,
                                                    vector_numbers_index, reduction_mode='pca')
    with codecs.open(PATH_TO_SAVE_DEEP_NN_RESULT, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_deepNN_pca, indent=4, ensure_ascii=False))


def generate_boy_position_deepNN():

    PATH_TO_INPUT_JSON = '../extracted/mr_collection/miss_member.json'
    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE = 'deep_learning/pylearn2_intermediate_files/boys_face_dmb'
    PATH_TO_DEEPNN_TRAINED = 'deep_learning/pylearn2_intermediate_files/boys_face_dmb/rbm.pickle/dbm.pkl'
    PROJECT_NAME = 'boys_face_dmb'
    PATH_TO_SAVE_DEEP_NN_RESULT = '../visualization/data_for_visual/mr_pics_deepNN_tsne_obj.json'

    # [-1] indicates to use all features
    vector_numbers_index = [-1]

    position_map_picture_deepNN = p_d.prepare_picture_matrix_with_deepNN_features(PATH_TO_INPUT_JSON,
                                                    PATH_TO_DEEPNN_TRAINED,
                                                    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE,
                                                    PROJECT_NAME,
                                                    vector_numbers_index, reduction_mode='t-sne')
    with codecs.open(PATH_TO_SAVE_DEEP_NN_RESULT, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_deepNN, indent=4, ensure_ascii=False))


    PATH_TO_SAVE_DEEP_NN_RESULT = '../visualization/data_for_visual/mr_pics_deepNN_pca_obj.json'
    position_map_picture_deepNN_pca = p_d.prepare_picture_matrix_with_deepNN_features(PATH_TO_INPUT_JSON,
                                                    PATH_TO_DEEPNN_TRAINED,
                                                    PATH_TO_DEEPNN_DATA_SOURCE_PICKLE,
                                                    PROJECT_NAME,
                                                    vector_numbers_index, reduction_mode='pca')
    with codecs.open(PATH_TO_SAVE_DEEP_NN_RESULT, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_deepNN_pca, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    #generate_girls_position()
    #generate_boys_position()
    generate_girls_position_deepNN()
    #generate_boy_position_deepNN()


