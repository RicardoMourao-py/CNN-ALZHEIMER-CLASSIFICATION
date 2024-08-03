import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.cloud import storage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

ENDPOINT_ID = "6177916142938488832"  # permanent_50_flowers_endpoint
PROJECT_ID = "bigdata-dados-publicos"
LOCATION = "us-central1"
API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
SENDER_EMAIL = "ricardomouraofilho@gmail.com"
SENDER_PASSWORD = os.environ['SENDER_PASSWORD_EMAIL']
RECEIVER_EMAIL = "ricardomouraofilho@gmail.com"

def download_image_from_bucket(bucket_name: str, blob_name: str) -> bytes:
    """Downloads an image from a Google Cloud Storage bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    image_data = blob.download_as_bytes()
    return image_data

def predict_image_classification(event, context):
    """Background Cloud Function to be triggered by Cloud Storage."""
    bucket_name = event['bucket']
    blob_name = event['name']

    print(f"Processing file: {blob_name} from bucket: {bucket_name}")

    # Download the image from the bucket
    image_data = download_image_from_bucket(bucket_name, blob_name)

    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": API_ENDPOINT}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(image_data).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5,
        max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=PROJECT_ID, location=LOCATION, endpoint=ENDPOINT_ID
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        out_predict = dict(prediction)
        print(" prediction:", out_predict)

    subject = "PREVISÃO DE CLASSIFICAÇÃO DE ALZHEIMER"
    body = str(out_predict)

    print("Cria a mensagem")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Conecta ao servidor SMTP")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        print("Envia o e-mail")
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)

        # Fecha a conexão
        server.quit()

        return 'Email enviado com sucesso!'
    except Exception as e:
        return str(e)

    
