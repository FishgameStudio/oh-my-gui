import threading

# Stores the current layout activated within the 'with' block, 
# and multiple threads do not interfere with each other.
active_layout = threading.local()