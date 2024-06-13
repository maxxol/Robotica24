class DataSender:

    def verstuur_object_coordinaten(self, object_coordinaten):
        objects = object_coordinaten[0], object_coordinaten[1], object_coordinaten[3][0], object_coordinaten[3][1], object_coordinaten[4][0], object_coordinaten[4][1]
        print(f"{object_coordinaten[0]} {object_coordinaten[1]} {object_coordinaten[3][0]} {object_coordinaten[3][1]} {object_coordinaten[4][0]} {object_coordinaten[4][1]}")
        result_string = f"{object_coordinaten[0][0]} {object_coordinaten[0][1]} {object_coordinaten[3][0]} {object_coordinaten[3][1]} {object_coordinaten[4][0]} {object_coordinaten[4][1]}"

        # Write the result string to the file
        with open("/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/results.txt", "w") as file:
            file.write(result_string)
        
        return

    def verstuur_target_coordinaten(self, target_coordinaten):
        print(target_coordinaten[0], target_coordinaten[1])
        return
