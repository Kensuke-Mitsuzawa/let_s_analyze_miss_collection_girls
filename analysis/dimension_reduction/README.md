# what's this?

This directory is scripts for dimension reduction.

Basically, in this directory, you can try

* QA document reduction with SVD
* picture matrix dimension reduction with tSNE
* picture matrix dimension reduction with PCA
* picture matrix dimension reduction with deepNN/PCA
 
# datamodel for output

as a output data, you can get following json datamodel.

This output data is an input data for visualization directory.

    {
        string: {
            "major": string, 
            "grade": int, 
            "age": int, 
            "member_name_rubi": string, 
            "height": float, 
            "member_index": int, 
            "profile_url": string, 
            "blog_url": string, 
            "member_name": string, 
            "university": string, 
            "position_vector": [
                float, 
                float
            ], 
            "photo_url": string
        }
 

# directory structure

* modules: scripts for reduction core
* document_reduction.py: dimension reduction for QA document
* picture_reduction.py: dimension reduction with face picutres