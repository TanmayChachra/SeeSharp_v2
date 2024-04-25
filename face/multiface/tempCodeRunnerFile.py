def find_target_face():
#     face_location = fr.face_locations(target_image)
#     count = 0
#     for person in encode_faces('C:/Users/Aarus/face/multiface/photos'):
#         encoded_face = person[0]
#         filename = person[1]
#         is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.55)
#         print(f'{filename} is {is_target_face}')
    
#         if face_location:
#             face_number = 0
#             for location in face_location:
#                 if is_target_face[face_number]:
#                     label = filename
#                     create_frame(location, label)
#                     count+=1
#                 face_number+=1
#     print("Total faces found: ", face_number)