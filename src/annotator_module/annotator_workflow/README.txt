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
