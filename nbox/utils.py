import unicodedata
import string
import os



################# TO CLEAN FILE NAMEs!! #######################
valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    for r in replace:
        filename = filename.replace(r,'_')
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    return ''.join(c for c in cleaned_filename if c in whitelist)

################## GRAPH CLASS ################################

graph_types = {"float" : float,
               "int": int}

class Graph:
    def __init__(self, name, dimensions=0, rewrite=True, delimiter=",", dtype=float):
        '''
                Actual graph class
                Usage:
                    name            : Name of the graph. This is also the file name for the graph.
                    dimensions      : Dimensions of the value. This is determined automatically if not specified.
                    rewrite         : If graph exist, does the user wish to rewrite the file.
                    Delimiter       : In case user wants to use a different delimiter.
                
                Basic Graph Structure:
                    name:<graph name>
                    dtype:<type value>
                    delimiter:<delimiter value>
                    values:
                    <values>
        '''


        self.name = name

        self.file_name = "./analysis/graphs/" + clean_filename(self.name) + ".txt"

        self.dimensions = dimensions
        self.delimiter = delimiter
        self.dtype = dtype
        
        if os.path.isfile(self.file_name):                          # Check if file already exist
            if rewrite:                                             # If user wants to rewrite, 
                with open(self.file_name, "w") as file:             # Rewrite the file
                    file.write("name:"+self.name+"\n")
                    file.write("dtype:"+str(self.dtype)[8:-2]+"\n")
                    file.write("delimiter:"+self.delimiter+"\n")
            else:                                                   # If he doesnt want to rewrite,
                temp_dimension = 0
                with open(self.file_name, "r") as file:             # Check the dimensions stored in previous graphs
                    lines = [_ for _ in file]
                    
                    self.dtype = graph_types[lines[1][6:-1]]          # Get Type for prvious file
                    self.delimiter = lines[2][10:-1]                 # Get delimiter for previous type

                    if len(lines) != 3:
                        last_line = lines[-1]
                        temp_dimension = len(last_line.split(self.delimiter))

                if self.dimensions != 0:                            # Check if use provided new dimesion and if it matches the old ones in the graph
                    assert (self.dimensions == temp_dimension), self.name  +"\nError: Previous dimensions stored does not match given dimensions. If you want to rewrite the file, please supply (rewrite=True)"
                
                self.dimensions = temp_dimension                    # set dimensions
        
        else:                                                       # Check if file doesnt exist
            with open(self.file_name, "w") as file:                 # Create the file
                file.write("name:"+self.name+"\n")
                file.write("dtype:"+str(self.dtype)[8:-2]+"\n")
                file.write("delimiter:"+self.delimiter+"\n")


    def add_point(self, values):
        try:
            len(values)
        except:
            values = [values]

        if self.dimensions == 0:                                    # If user didn't specify the dimension, automatically set it with first value given by the user
            self.dimensions = len(values)                           

        # print(self.dimensions, len(values))
        assert (self.dimensions == len(values)), "Error: Previous dimensions stored does not match given dimensions."                   # Check if the dimension of value provided by the user is same as before. 

        with open(self.file_name, "a+") as file:
            write_string = ""
            for _ in values:
                write_string += str(_) + ","
            write_string = write_string[:-1] + "\n"
            file.write(write_string)

    def add_points(self, values):
        for value in values:
            self.add_point(value)

################## PLOT FUNCTION ################################

def save_plot(plt, name=""):
    """
        Plots given matplotlib.pyplot object as an image. The image is saved in ./analysis/images folder.
        All the images saved in ./analysis/images are automatically displayed in browser.

        Arguments:
            - plt: matplotlib.pyplot object
            - name: Name of the graph. It is automatically set if not given,
    """

    if name == "":
        temp = 0
        while name == "":
            temp += 1
            if not os.path.isfile("./analysis/images/Fig_"+str(temp) + ".png"):
                name = "./analysis/images/Fig_"+str(temp) + ".png"

    else:
        name = clean_filename(name)
        name = "./analysis/images/" + name + ".png"

    plt.savefig("test.png", dpi=400, pad_inches=0.3, bbox_inches='tight')


################## IMAGE SAVE FUNCTION ##########################
import numpy as np
import cv2
image_formats = ["png", "jpg", "bmp"]


def im_save(image, name="", image_format="RGB"):
    image = np.array(image)
    if name == "":
        temp = 0
        while name == "":
            temp += 1
            if not os.path.isfile("./analysis/images/Image_" + str(temp) + ".png"):
                name = "./analysis/images/Image_" + str(temp) + ".png"
    else:
        type_ = name.split(".")[-1]
        if type_ in image_formats:
            name = "./analysis/images/" + name
        else:
            name = "./analysis/images/" + name + ".png"
    
    if image_format == "RGB":
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(name, image)
    
    else:
        cv2.imwrite(name, image)
