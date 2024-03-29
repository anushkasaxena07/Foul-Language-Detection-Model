#!/usr/bin/env python
# coding: utf-8

# # Foul Detection Model

# In[2]:


import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer

# Assuming cv is your CountVectorizer instance
cv = CountVectorizer()

# Load foul_detector_model with try-except block
try:
    md = joblib.load("foul_detector_model.joblib")
    
    # Get the absolute path to the current directory
    current_directory = os.path.abspath(os.getcwd())
    
    # Construct the absolute path to the vocabulary file
    vocabulary_path = os.path.join(current_directory, "vocabulary.joblib")
    
    # Check if the vocabulary file exists before loading
    if os.path.exists(vocabulary_path):
        # Load the vocabulary
        vocabulary = joblib.load(vocabulary_path)
        
        # Set the vocabulary for CountVectorizer
        cv.vocabulary_ = vocabulary
    else:
        print("Vocabulary file not found.")
    
except (ValueError, KeyError) as e:
    print(f"Error loading the model or vocabulary: {e}")
    # Additional troubleshooting or fallback action may be needed here
    # You might want to retrain and save the model if there are no compatibility issues

def detect(test_data):
    # Assuming the model was trained with the same CountVectorizer instance
    df = cv.transform([test_data]).toarray()
    m = int(md.predict(df))
    return m


# # Voice detection model

# In[3]:


import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models, callbacks


# In[4]:


# Function to extract features from audio data
def extract_features(file_path):
    audio_data, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
    return np.mean(mfccs, axis=1)


# In[5]:


# Load the model
loaded_model = models.load_model('speaker_identification_model.h5')

# Load the label encoder
loaded_label_encoder = LabelEncoder()
loaded_label_encoder.classes_ = np.load('label_encoder.npy')

def Recog_voice(new_audio_file_wav):
    # Example: Get predictions for a new WAV audio file
    #new_audio_file_wav = 'd_v.wav'
    new_features_wav = extract_features(new_audio_file_wav)

    # Reshape the input data to match the model's input shape
    new_features_reshaped_wav = new_features_wav.reshape(1, len(new_features_wav), 1)

    # Make predictions
    predictions_wav = loaded_model.predict(new_features_reshaped_wav)  # Use loaded_model instead of model

    # Get the index with the highest predicted value
    predicted_index_wav = np.argmax(predictions_wav)

    # Decode the predicted labels using the loaded label encoder
    predicted_label_wav = loaded_label_encoder.inverse_transform(np.array([predicted_index_wav])).reshape(1, -1)

    print(f'Predicted Speaker: {predicted_label_wav[0]}')
    return predicted_label_wav[0]


# # Storing Database

# In[6]:


import cv2
import librosa
import numpy as np
import mysql.connector


# In[7]:


def storedata(audio_file_path):   
    mydb = mysql.connector.connect(
        host ="localhost",
        user ="root",
        password ="8871@Ajay",
        database = "Foul_DB"
    )

   
    cur = mydb.cursor()

    # cur.execute("CREATE TABLE Students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL)")

    #cur.execute("CREATE TABLE Defaulters_list (ID INT PRIMARY KEY, audio VARCHAR(255) NOT NULL, fine DECIMAL(10, 2) NOT NULL, FOREIGN KEY (ID) REFERENCES Students(id))")

    # Uncomment the next line if you're inserting data into the Students table
    # cur.execute("INSERT INTO Students (name) VALUES ('Kratika')")


    # Execute the SELECT query
    select_query = f"SELECT id FROM Students WHERE name='{S_name[0]}'"
    cur.execute(select_query)

    # Fetch the result
    result = cur.fetchone()

    # Check if result is not None
    if result:
        student_id = result[0]
        fine=100
        # Use Binary class to handle binary data
        insert_query = "INSERT INTO Defaulters_list (ID,audio,fine) VALUES (%s, %s,%s)"
        cur.execute(insert_query, (student_id,audio_file_path,fine))

        # Commit the changes
        mydb.commit()
    else:
        print("No student found with the given name.")

    # Close the cursor
    cur.close()
   


# # Dashboard

# In[ ]:


import os
import speech_recognition as sr

class Dashboard:
    
    def __init__(self, save_folder="audio_inputs"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)
        self.count = 0  # Initialize count as an instance variable

    @staticmethod  # Use static method as it doesn't depend on instance data
    def uniquecode():
        count_file_path = "count.txt"

        with open(count_file_path, "r") as count_file:
            count = int(count_file.read())  # Read count from file

        with open(count_file_path, "w") as count_file:
            count += 1  # Increment count
            count_file.write(str(count))  # Write updated count to file

        return count

    def convert_audio_to_text(self):
        current_uniquecode = self.uniquecode()

        # Specify the folder path to save the audio file
        audio_file_path = os.path.join(self.save_folder, f"audio_input_{current_uniquecode}.wav")

        with self.microphone as source:
            print("Listening...")
            try:
                audio_data = self.recognizer.listen(source, timeout=5)  # Adjust timeout as needed
                # Save the audio data to a file
                with open(audio_file_path, "wb") as audio_file:
                    audio_file.write(audio_data.get_wav_data())

                text = self.recognizer.recognize_google(audio_data)
                return text, audio_file_path
            except sr.UnknownValueError:
                return "Could not understand audio", None
            except sr.RequestError as e:
                return f"Error connecting to Google API: {e}", None

# Example usage:
if __name__ == "__main__":
    # Specify the custom folder path
    custom_folder_path = "audio_inputs"

    # Create an instance of Dashboard with the custom folder path
    dashboard = Dashboard(save_folder=custom_folder_path)

    # Example usage:
    result, audio_file_path = dashboard.convert_audio_to_text()

    if audio_file_path:
        print("Text from audio:")
        print(result)

        # Example usage of undefined functions
        output = detect(result)
        if output==0:
            print("Status: All Good")
        else:
            # Pass the captured audio file path to Recog_voice (replace with your actual function)
            print("Status: Foul Detected")
            S_name = Recog_voice(audio_file_path)
            storedata(audio_file_path)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[13]:





# In[16]:





# In[11]:





# In[ ]:





# In[ ]:





# In[ ]:




