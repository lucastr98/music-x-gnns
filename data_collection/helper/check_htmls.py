import os

# # related artists
# folder_path = '../../data/htmls/relatedArtists'
# required_string = 'relatedArtistsSidebarLink'
# optional_strings = [
#     'related similars clearfix',
#     'related collaboratorwith clearfix',
#     'related influencers clearfix',
#     'related followers clearfix',
#     'related associatedwith clearfix',
# ]

# songs 
folder_path = '../../data/htmls/songs'
required_string = 'songsSidebarLink'
optional_strings = [
    'songTitle'
]

# Function to check if conditions are met in the content of a file
def check_conditions(content):
  if required_string in content:
    return any(optional_string in content for optional_string in optional_strings)
  return True

# Loop through each file in the folder
for filename in os.listdir(folder_path):
  file_path = os.path.join(folder_path, filename)
  if os.path.isfile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
      content = file.read()
      if not check_conditions(content):
        print(filename)
