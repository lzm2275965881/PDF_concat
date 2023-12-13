
import PyPDF2
import tkinter as tk
from tkinter import filedialog

class PDFJoinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Joiner")

        self.pdf_files = [[None for _ in range(6)] for _ in range(6)]
        self.horizontal_spacing = tk.DoubleVar(value=0.0)  # 默认横向间距为0
        self.vertical_spacing = tk.DoubleVar(value=0.0)    # 默认纵向间距为0
        # self.horizontal_spacing = 0
        # self.vertical_spacing = 0
        self.grid_size = 5
        # 创建界面元素
        tk.Label(root, text="PDF Joiner(by LZM)", font=("Helvetica", 16)).grid(row=0, columnspan=6, pady=10)

        # 创建选择文件的按钮
        self.buttons = []
        for i in range(self.grid_size):
            button_row = []
            for j in range(self.grid_size):
                button = tk.Button(root, text=f"Select PDF {i+1}-{j+1}", command=lambda i=i, j=j: self.select_pdf(i, j))
                button.grid(row=i+1, column=j, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        # 输入框和标签用于设置横向和纵向间距
        tk.Label(root, text="横向间距:").grid(row=8, column=0, pady=1, sticky="e")
        tk.Entry(root, textvariable=self.horizontal_spacing).grid(row=8, column=1, pady=1, sticky="w")
        tk.Label(root, text="纵向间距:").grid(row=8, column=2, pady=1, sticky="e")
        tk.Entry(root, textvariable=self.vertical_spacing).grid(row=8, column=3, pady=1, sticky="w")


        tk.Button(root, text="清除选择", command=self.clear_selection).grid(row=0, columnspan=1, pady=10)
        tk.Button(root, text="拼接", command=self.join_pdfs).grid(row=7, columnspan=9, pady=10)


    def clear_selection(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.pdf_files[i][j] = None
                self.buttons[i][j].config(bg="SystemButtonFace")  # 恢复默认按钮颜色


    def select_pdf(self, row, col):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_files[row][col] = file_path
            print(f"Selected PDF {row+1}-{col+1}: {file_path}")

            # 更改按钮颜色为已选择的颜色
            self.buttons[row][col].config(bg="lightgreen")

    def join_pdfs(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        print(output_path)
        if output_path:
            self.concatenate_pdfs(self.pdf_files, output_path)
            print(f"PDFs joined. Output: {output_path}")

    #@staticmethod
    def concatenate_pdfs(self,input_files, output_file):
        horizontal_spacing = self.horizontal_spacing.get()
        vertical_spacing = self.vertical_spacing.get()
        pdf_writer = PyPDF2.PdfFileWriter()

        page = []
        max_widths = []
        max_heights = []
        max_height = 0
        max_width = 0
        for row in range(self.grid_size):
            max_height = 0
            for col in range(self.grid_size):
                file_path = input_files[row][col]
                if file_path:
                    print(file_path)
                    pdf_reader = PyPDF2.PdfFileReader(open(file_path, 'rb'))
                    page = pdf_reader.getPage(0)
                    height = page.mediaBox.getHeight()
                    if max_height < height:
                        max_height = height
            max_heights.append(max_height)
        for col in range(self.grid_size):
            max_width = 0
            for row in range(self.grid_size):
                file_path = input_files[row][col]
                if file_path:
                    print(file_path)
                    pdf_reader = PyPDF2.PdfFileReader(open(file_path, 'rb'))
                    page = pdf_reader.getPage(0)
                    width = page.mediaBox.getWidth()
                    if max_width < width:
                        max_width = width
            max_widths.append(max_width)
                    #pdf_writer.addPage(pdf_reader.getPage(0))  # Add only the first page
        # print(len(max_heights>0),len(max_widths>0))
        width_page = sum(1 for x in max_widths if x > 0)
        height_page = sum(1 for x in max_heights if x > 0)
        print(width_page, height_page)
        new_width_horizontal = sum(max_widths)# + width3# + width4
        new_height_horizontal = sum(max_heights)
        interval_witdh = int(horizontal_spacing*int(max(max_widths)))
        interval_height = int(vertical_spacing*int(max(max_heights)))
        new_width_horizontal += interval_witdh*(width_page-1)
        new_height_horizontal += interval_height*(height_page-1)
        pdf_writer_horizontal = PyPDF2.PdfFileWriter()
        new_page_horizontal = pdf_writer_horizontal.addBlankPage(new_width_horizontal, new_height_horizontal)
        for col in range(self.grid_size):
            for row in range(self.grid_size):
                file_path = input_files[row][col]
                if file_path:
                    pdf_reader = PyPDF2.PdfFileReader(open(file_path, 'rb'))

                    new_page_horizontal.mergeTranslatedPage(pdf_reader.getPage(0),sum(max_widths[:col])+col*interval_witdh, sum(max_heights[row+1:])+(height_page-row-1)*interval_height)
        with open(output_file, 'wb') as output_pdf:
            pdf_writer_horizontal.write(output_pdf)

#if __name__ == "__main__":
root = tk.Tk()
app = PDFJoinerApp(root)
root.mainloop()