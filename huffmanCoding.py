
import heapq , os

class HuffmanCoding:


    def __init__(self , path):
        self.path = path
        self.heap = []
        self.code = {}
        self.reversecode = {}

    class BinaryTree:

        def __init__(self, value , frequency):
            self.value = value
            self.freq = frequency
            self.left = None
            self.right = None
        
        def __lt__(self , other):
            return self.freq < other.freq
        
        def __eq__(self , other):
            if(other == None):
                return False
            if(not isinstance(other ,BinaryTree)):
                return False
            
            return self.freq == other.freq

    # calculate frequency and return 
    def make_frequency_dict (self, text):
        fre_dic = {}

        for char in text:
            if char not in fre_dic:
                fre_dic[char] = 0
            fre_dic[char] += 1
        return fre_dic
    

    # make priorityqueue
    def make_heap(self , frequency_dictionary):
        for key in frequency_dictionary:
            frequency = frequency_dictionary[key]
            binary_tree_node = self.BinaryTree(key , frequency)
            heapq.heappush(self.heap , binary_tree_node)

    def merge_codes_build_binary_tree(self):

        while (len(self.__heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            sum_of_freq = node1.freq + node2.freq
            newNode = self.BinaryTree(None , sum_of_freq)
            newNode.left = node1
            newNode.right = node2
            heapq.heappush(self.heap , newNode)

        return     

    
    def make_codes_helper(self , root , current_code):
        
        if root is None:
            return
        
        if root.value is not None:
            self.code[root.value] = current_code
            self.reversecode[current_code] = root.value
        
        self.make_codes_helper(root.left ,current_code +'0')
        self.make_codes_helper(root.right ,current_code +'1')

    def make_codes_from_binary_tree(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root , current_code)



    def get_encoded_text(self , text):
        encoded_text = ''

        for char in text:
            encoded_text += self.code[char]

        return encoded_text
        
    def pad_encoded_text(self , encoded_text):
        padding_value = 8 - len(encoded_text)  % 8
        for i in range(padding_value):
            encoded_text += '0'

        padded_info = "{0:08b}".format(padding_value)
        padded_text = padded_info + encoded_text
        return padded_text
    

    def get_byte_array(self , padded_text):
        array = bytearray()
        for i in range(0 , len(padded_text) , 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))

        return array
    


    def compress(self):

        

        print("compression for your file starts....")

        # to access the file and extract text from that file

        filename, file_extension = os.path.splitext(self.path)
        # output file named as same name and binary file
        output_path = filename + '.bin'

        with open(self.path , 'r') as file , open(output_path , 'wb') as output:
            text = file.read()
            text = text.rstrip() # to trim the extra spaces

            frequency_dictionary = self.make_frequency_dict(text)
            # calculate the frequency of each text and store it in dictionary

            
            build_heap = self.make_heap(frequency_dictionary)
            # Min heap for two minimum frequency
            # construct binary tree from heap

            self.merge_codes_build_binary_tree()
            # construct code from binary tree and stored it in dictionary
            self.make_codes_from_binary_tree()

            # construct encoded text 
            encoded_text = self.get_encoded_text(text)

            # padding of encoded text

            padded_text = self.pad_encoded_text(encoded_text)
            # we have to return that binary file as an output
            bytes_array = self.get_byte_array(padded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        print('compressed successfully')
        return output_path
    




    def remove_padding(self , text):
        padded_info = text[:8]
        padding_value = int(padded_info , 2)
        text = text[8:]
        text = text[:-1*padding_value]
        return text
    
        
    def decode_text(self , text):
        current_code = ''
        decoded_text = ''
        for char in text:
            current_code += char
            if current_code in self.reversecode:
                decoded_text += self.reversecode[current_code]
                current_code = ''
        return decoded_text
    

    def decompress(self ,input_path):

        filename , file_extension = os.path.splitext(input_path)
        output_path = filename + '_decompressed' + '.txt'
        with open(input_path , 'rb') as file , open (output_path , 'w') as output:
            bit_string = ''
            byte = file.read(1)
            while(len(byte) >0):
                byte = ord(byte) #ord (arg) is used to convert hexadecimal into integer
                bits = bin(byte)[2:].rjust(8 , '0') #bin(arg) integer to -----> binary
                 # slicing is done beacause it is in the form of B'0111... to remove the "B'"
                # rjust() used to convert it into 8bit format 
                bit_string += bits
                byte = file.read(1)

            text_after_removing_padding = self.remove_padding(bit_string) 
            actual_text = self.decode_text(text_after_removing_padding)
            output.write(actual_text)
        print("Decompressed")
        return output_path
    

path = input("Enter the path of your file which you need to compress")
h = HuffmanCoding(path)
compressed_file = h.compress()
h.decompress(compressed_file)