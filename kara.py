#made by Timo654, thx to etra0 and MnSxX for help
import sys

#karaoke files seem to only be big endian
ENDIANNESS = 'big'

input_files = sys.argv[1:]
#checks if there are any files
if input_files == []:
    input("No files detected. You need to drag and drop the file.\nPress any key to continue.")
    quit()

#saves new file
def save_files(input_files, binary_data):
    with open(input_files + '-new.bin', 'wb') as f:
        f.write(binary_data)
        print(input_files + "-new.bin saved.")

#loads the file
def load_file(input_files):
    global binary_data
    with open(input_files, 'rb') as binary_file:
        binary_data = bytearray(binary_file.read())
    version_check(input_files)

#gets info about header, first offset and number of lyrics from files
def get_files(input_files):
        if version == "y4":
            print("Yakuza 4/Dead Souls karaoke file found.")
            f_o = 0x66 #first offset
            header = int.from_bytes(binary_data[0x6:0x8], ENDIANNESS)
            n_lyrics = int.from_bytes(binary_data[0x6:0x7], ENDIANNESS)
        else:
            print("Yakuza 5/Ishin/Zero/Kiwami karaoke file found.")
            f_o = 0x56 #first offset
            header = int.from_bytes(binary_data[0x10:0x12], ENDIANNESS)
            n_lyrics = int.from_bytes(binary_data[0x10:0x11], ENDIANNESS)
        edit_files(binary_data, header, n_lyrics, f_o, input_files)

#checks version
def version_check(input_files):
    global version
    #verifies if this is actually a karaoke file
    if not binary_data[0x00:0x04].decode().strip('\x00') == 'KARA':
        input("Not a valid karaoke file.\nPress any key to continue.")
        quit()
    check_version = int.from_bytes(binary_data[0x6:0x8], ENDIANNESS)
    if check_version == 0:
        version = 'y5'
    else:
        version = 'y4'
    get_files(input_files)
#edits header and offsets
def edit_files(binary_data, header, n_lyrics, f_o, input_files):
    total_offsets = n_lyrics * 3
    offsets_changed = 1
    if version == 'y4': #edits header to convert Yakuza 3 karaoke songs to Yakuza 5 format
        binary_data[0x10:0x10] = bytearray([0]*16)
        binary_data[0x10:0x12] = header.to_bytes(2, byteorder=ENDIANNESS) #adds new header
        binary_data[0x6:0x8] = bytearray([0]*2) #deletes old header
    else: #edits header to convert Yakuza 5 karaoke songs to Yakuza 3 format
        binary_data[0x6:0x8] = header.to_bytes(2, byteorder=ENDIANNESS)
        binary_data[0x10:0x21] = bytearray([0]*1)
    while offsets_changed <= total_offsets:
        if offsets_changed % 3 == 0:
            offset = 24
        else: offset = 8
        current_offset = int.from_bytes(binary_data[f_o:f_o+2], ENDIANNESS)
        if version == 'y4': #due to header changes, we need to change all offsets
            current_offset += 16
        else: current_offset -= 16
        binary_data[f_o:f_o+2] = current_offset.to_bytes(2, byteorder=ENDIANNESS)
        f_o = f_o + offset
        offsets_changed += 1
    save_files(input_files, binary_data)

#reads file
for file in input_files:
    load_file(file)

input("Files successfully converted.\nPress enter to continue...")