
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR
source ../venv/bin/activate
python manage.py scrapper1

# 52 14 * * * /bin/bash /media/nikunj/CAF28011F28003C3/ecom_django_mongo/ecommerce/task/task.sh >> /media/nikunj/CAF28011F28003C3/ecom_django_mongo/ecommerce/log/cronlog.log 2>&1