### Some Requirements:###
create a file named supervisely.env in /home/user/supervisely.env like this:
SERVER_ADDRESS = "https://YOUR_SUPERVISELY_DOMAIN.com"
API_TOKEN = "YOUR SUPERVISELY TOKEN"
######################################
Follow the instructions here to be able to access some of the gsheet files through codes:
11/13 steps explained by desaiankitb
https://stackoverflow.com/questions/62917910/how-can-i-export-pandas-dataframe-to-google-sheets-using-python
######################################
######################################
######################################
######################################
FOR THE ANNOTATION WORKSFLOW:

0-
You have to create a json file in which the video names and the tag numbers are specified in a dictionary.
See examples in PROJECT_PATH/data/Evaluations_json
#######################
1-
python incisionDataFolderCreation.py --batch 4 --output annotationDatas/annotationData4 --project Endometriosis_WS2 --annotator nicolas.bourdel
and repeat this for all other annotators then you have folders inside --output parameters for each of these annotators
#######################
2-
python incisionComparison_V5.py --input annotationDatas/annotationData4 --batch 4
in a folder called ImagOut you have the visualizations ready for the annotators
########################
Before step 2 there are other process that can be done depending on what you want to visualize:
-If you want to also visualize machine predictions:

-If you want to also visualize STAPLE:

##########################
