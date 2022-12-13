
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR
source ../venv/bin/activate
python manage.py scrapper2


