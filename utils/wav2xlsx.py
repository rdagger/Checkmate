import wave
import openpyxl

# Function to convert a wave file to an Excel spreadsheet
def wave_to_excel(input_wave_file, output_excel_file):
    # Open the wave file for reading
    with wave.open(input_wave_file, 'rb') as wave_file:
        # Create a new Excel workbook and select the default sheet
        wb = openpyxl.Workbook()
        ws = wb.active

        # Create a header row
        ws.append(["Sample Index", "Amplitude"])

        # Read and write raw wave data to the spreadsheet
        for i in range(wave_file.getnframes()):
            # Read a single frame (sample)
            frame = wave_file.readframes(1)
            if not frame:
                break

            # Convert the binary data to an integer
            sample = int.from_bytes(frame, byteorder='little', signed=True)

            # Write the sample index and amplitude to the spreadsheet
            ws.append([i, sample])

        # Save the Excel file
        wb.save(output_excel_file)

if __name__ == "__main__":
    input_wave_file = "P3_down.wav"      # Replace with your input wave file
    output_excel_file = "P3_down.xlsx"  # Replace with your desired output Excel file

    wave_to_excel(input_wave_file, output_excel_file)
    print(f"Wave data converted and saved to {output_excel_file}")
