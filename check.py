import tensorflow.compat.v1 as tf

# Path to the checkpoint file
checkpoint_path = "C:/Users/shifz/OneDrive/Desktop/lip_frontend/models/checkpoint"

try:
    # List all variables in the checkpoint file
    checkpoint_vars = tf.train.list_variables(checkpoint_path)
    
    # Print the variable names and shapes
    for var_name, var_shape in checkpoint_vars:
        print(f"Variable: {var_name}, Shape: {var_shape}")

except Exception as e:
    print(f"Error: {e}")
    print("Failed to list variables in the checkpoint file.")
