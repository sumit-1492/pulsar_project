import os
import sys
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask,request,send_file,abort,render_template
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.utils.common import create_directories
from pulsarclassification.pipeline.stage_07_model_prediction import InstanceData,BatchData,ModelPredict
from pulsarclassification.constants import *

pulsar_predict = ModelPredict()

prediction_data_directory = os.path.join(ROOT_DIR,MODEL_PREDICTION_ARTIFACT_DIR_NAME)
create_directories(prediction_data_directory)

batch_data_directory = os.path.join(prediction_data_directory,"BatchData")
create_directories(batch_data_directory)

instance_data_directory = os.path.join(prediction_data_directory,"InstanceData")
create_directories(instance_data_directory)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        raise PulsarException(e,sys)
    
@app.route('/train', methods=['GET', 'POST'])
def train():
    try:
        os.system("python main.py")
        message='Model Training Stage Completed'

        return render_template('index.html', message=message)
    except Exception as e:
            raise PulsarException(e,sys)
    
@app.route('/instance', methods=['GET', 'POST'])
def predict():
    try:
        if request.method == 'GET':
            return render_template('predict.html')
        else:

            Mean_Integrated = float(request.form['Mean_Integrated'])
            SD = float(request.form['SD'])
            EK = float(request.form['EK'])
            Skewness = float(request.form['Skewness'])
            Mean_DMSNR_Curve = float(request.form['Mean_DMSNR_Curve'])
            SD_DMSNR_Curve = float(request.form['SD_DMSNR_Curve'])
            EK_DMSNR_Curve = float(request.form['EK_DMSNR_Curve'])
            Skewness_DMSNR_Curve = float(request.form['Skewness_DMSNR_Curve'])
        

            pulsar_data = InstanceData(Mean_Integrated=Mean_Integrated,
                                    SD=SD,
                                    EK=EK,
                                    Skewness=Skewness,
                                    Mean_DMSNR_Curve=Mean_DMSNR_Curve,
                                    SD_DMSNR_Curve=SD_DMSNR_Curve,
                                    EK_DMSNR_Curve=EK_DMSNR_Curve,
                                    Skewness_DMSNR_Curve=Skewness_DMSNR_Curve
                                        )
            
            pulsar_df = pulsar_data.get_instance_data_frame()

            instance_data_save_dir = os.path.join(instance_data_directory,MODEL_PREDICTION_INSTANCE_DIR_NAME)
            create_directories(instance_data_save_dir)

            pulsar_df.to_csv(os.path.join(instance_data_save_dir,"pulsar_instant_data.csv"),index=False)

            pulsar_predicton_result = pulsar_predict.predict(pulsar_df)

            pulsar_df['predicted_model_result'] = pulsar_predicton_result

            pulsar_df.to_csv(os.path.join(instance_data_save_dir,INSTANCE_CSV_FILE_NAME),index=False)

            logging.info(f"=============== Instance data saved in : {instance_data_save_dir} ===============")

            logging.info(f"=============== Instance prediction log completed ===============")


        return render_template("predict.html",pulsar_value = pulsar_predicton_result)
    
    except Exception as e:
                raise PulsarException(e,sys)
    
ALLOWED_EXTENSIONS={'csv'}
@app.route('/batch', methods=['GET', 'POST'])
def perform_batch_prediction():
    if request.method == 'GET':
        return render_template('batch.html')
    else:
    
        batch_data_save_dir = os.path.join(batch_data_directory,MODEL_PREDICTION_BATCH_DIR_NAME)
        create_directories(batch_data_save_dir)

        file = request.files['csv_file']  # Update the key to 'csv_file'

        # Check if the file has a valid extension
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            
            # Save the new file to the uploads directory
            filename = secure_filename(file.filename)
            file_path = os.path.join(batch_data_save_dir, filename)
            file.save(file_path)
            print(file_path)
            logging.info(f"CSV received and Uploaded in : {file_path}")

            # Perform batch prediction using the uploaded file
            pulsar_batch_data = BatchData(file_path)
            pulsar_batch_df = pulsar_batch_data.get_batch_data_transformation()
            
            pulsar_predicton_result = pulsar_predict.predict(pulsar_batch_df)
            
            pulsar_batch_df['predicted_model_result'] = pulsar_predicton_result

            pulsar_batch_df.to_csv(os.path.join(batch_data_save_dir,BATCH_CSV_FILE_NAME),index=False)

            logging.info(f"=============== Batch data saved in : {batch_data_save_dir} ===============")

            logging.info(f"=============== Batch prediction log completed ===============")
            
            output = "Batch Prediction Done"

            return render_template("batch.html", prediction_result=output, prediction_type='batch')
        else:
            return render_template('batch.html', prediction_type='batch', error='Invalid file type')
        

if __name__ == "__main__":
    app.run(port=8000)