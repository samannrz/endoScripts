# examples/usage.sh
#!/bin/bash
cd "$(dirname "$0")/.." || exit

echo "Extracting annotation of the user: nicolas bordel for a pecific batch #4..."
python -m src.annotator_module.annotator_workflow.incisionDataFolderCreation\
    --batch 4 \
    --output annotationDatas/annotationData4 \
    --project Endometriosis_WS2 \
    --annotator nicolas.bourdel


python incisionDataFolderCreation.py --batch 4 --output annotationDatas/annotationData4 --project Endometriosis_WS2 --annotator nicolas.bourdel
and repeat this for all pther annotators