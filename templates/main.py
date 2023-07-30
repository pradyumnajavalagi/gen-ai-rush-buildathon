import numpy as np
import matplotlib.pyplot as plt
import zipfile
from matplotlib.animation import FuncAnimation

# Generate random ECG-like data for demonstration
num_samples = 1000
num_points = 4096
num_leads = 12
ecg_data = np.random.rand(num_samples, num_points, num_leads) * 0.5  # Scaling for demonstration purposes

# Normalize the data by multiplying by 1000 (assuming it's at the scale 1e-4V)
ecg_data *= 1000

# Save the ECG data to a zip file
with zipfile.ZipFile("sample2017.zip", "w") as myzip:
    with myzip.open("ecg_data.npy", "w") as myfile:
        np.save(myfile, ecg_data)

# Now, let's extract the data from the zip file and load it back into a variable
extracted_data = None
with zipfile.ZipFile("sample2017.zip", "r") as myzip:
    with myzip.open("ecg_data.npy") as myfile:
        extracted_data = np.load(myfile)

# Verify that the extracted data matches the original data
print("Original data shape:", ecg_data.shape)
print("Extracted data shape:", extracted_data.shape)

# Check if the data matches (ignoring numerical precision)
print("Data matches:", np.allclose(ecg_data, extracted_data))

# Set up the ECG graph for animation
lead_index = 0  # Start with DI lead
sample_index = 0  # First sample in the dataset (you can change this index to visualize other samples)

time_points = np.arange(0, num_points) / 400.0  # Sampling rate is 400 Hz

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(time_points, extracted_data[sample_index, :, lead_index], color='green')
ax.set_title(f"Moving ECG Graph - Sample {sample_index}, Lead DI")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Voltage (mV)")
ax.set_ylim(0, 1000)  # Adjust y-axis limit to 0 to 1000
ax.set_xlim(0, 0.1)  # Adjust x-axis limit to 0 to 0.5
ax.grid(True)
ax.set_facecolor('black')  # Set background color to black

# Function to update the plot with new data for animation
def update(frame):
    global lead_index
    lead_index = (lead_index + 1) % num_leads  # Move to the next lead in a cyclic manner
    line.set_ydata(extracted_data[sample_index, :, lead_index])
    ax.set_title(f"Moving ECG Graph - Sample {sample_index}, Lead {lead_index+1}")
    return line,

# Animate the ECG graph with a slower animation speed (interval set to 500 milliseconds)
ani = FuncAnimation(fig, update, frames=num_leads, interval=500)

# Function to classify ECG data using the if-else based prediction method
def predict_heart_disease(heart_rate, st_segment_changes, qrs_duration):
    if heart_rate > 700:
        return "Arrhythmias"
    elif st_segment_changes == 'elevated':
        return "Myocardial Infarction (Heart Attack)"
    elif qrs_duration > 720:
        return "Ischemic Heart Disease (Coronary Artery Disease)"
    elif heart_rate < 60:
        return "Cardiomyopathies"
    elif st_segment_changes == 'depressed':
        return "Heart Block"
    elif qrs_duration > 400 and qrs_duration <= 420:
        return "Long QT Syndrome"
    else:
        # Random prediction for demonstration (replace with your actual prediction method)
        import random
        pat = ["heart problem", "no heart problem", "no heart problem"]
        return random.choice(pat)

# Assuming you have collected and preprocessed the user's ECG data
user_heart_rate = 80
user_st_segment_changes = 'normal'
user_qrs_duration = 90

# Predict the heart disease type using the if-else based method
predicted_disease = predict_heart_disease(user_heart_rate, user_st_segment_changes, user_qrs_duration)

# Display the result to the user
print(f"Predicted Disease: {predicted_disease}")

# To display the animation and ECG prediction in a standalone Python script
plt.show()