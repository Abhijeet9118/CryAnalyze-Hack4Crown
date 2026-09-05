import tensorflow as tf
import os

def convert_to_tflite(model_path="models/cry_model.h5", output_path="models/cry_model.tflite"):
    """
    Converts a trained Keras/TensorFlow H5 model into TensorFlow Lite (.tflite) format.
    TFLite models are lightweight, quantized, and optimized to run 100% offline on
    mobile devices, edge hardware, or local CPUs without internet or GPUs.
    """
    if not os.path.exists(model_path):
        print(f"Model file '{model_path}' not found. Please train or place your model in models/")
        return

    # Load Keras Model
    model = tf.keras.models.load_model(model_path)

    # Initialize TFLite Converter
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Enable Default Quantization (reduces model size by ~4x, speeds up offline CPU inference)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    # Convert Model
    tflite_model = converter.convert()

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(tflite_model)

    print(f"Offline TFLite model saved successfully at: {output_path}")

if __name__ == "__main__":
    convert_to_tflite()
