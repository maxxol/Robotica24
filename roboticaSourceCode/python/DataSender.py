class DataSender:

    def verstuur_object_coordinaten(self, object_coordinaten):
        # Form the string to be written to the file
        result_string = f"{object_coordinaten[0][0]} {object_coordinaten[0][1]} {object_coordinaten[3][0]} {object_coordinaten[3][1]} {object_coordinaten[4][0]} {object_coordinaten[4][1]}"

        # Define the file path
        file_path = "/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/results.txt"

        # Write the result string to the file
        with open(file_path, "w") as file:
            file.write(result_string)
        print(f"{object_coordinaten[0]} {object_coordinaten[1]} {object_coordinaten[3][0]} {object_coordinaten[3][1]} {object_coordinaten[4][0]} {object_coordinaten[4][1]}")
        return

    def verstuur_target_coordinaten(self, target_coordinaten):

        return



