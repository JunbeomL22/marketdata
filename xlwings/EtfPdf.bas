Attribute VB_Name = "EtfPdf"
Option Explicit

Public Sub LoadEtfPdf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim dt As String
    Dim pdf_file As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "EtfPdf"
    Set this_sht = Sheets(sheet_name)

    dt = this_sht.Range("C4").Value
    pdf_file = this_sht.Range("C6").Value
    output_head = this_sht.Range("C7").Value
    ' clear the output range 20,000 rows and 30 columns from the output head
    this_sht.Range(output_head).Resize(20000, 30).ClearContents

    python_code = "import etf_pdf;"
    python_code = python_code + "etf_pdf.load_etf_pdf(dt = '" & dt & "', "
    python_code = python_code + "sheet_name = '" & sheet_name & "', "
    python_code = python_code + "pdf_file = '" & pdf_file & "', "
    python_code = python_code + "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveEtfPdf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim dt As String
    Dim base_info_file As String
    Dim pdf_file As String
    Dim python_code As String

    sheet_name = "EtfPdf"
    Set this_sht = Sheets(sheet_name)

    dt = this_sht.Range("C4").Value
    base_info_file = this_sht.Range("C5").Value
    pdf_file = this_sht.Range("C6").Value
    
    python_code = "import etf_pdf;"
    python_code = python_code + "etf_pdf.save_etf_pdf(dt = '" & dt & "', "
    python_code = python_code + "base_info_file = '" & base_info_file & "', "
    python_code = python_code + "pdf_file = '" & pdf_file & "')"
    
    RunPython python_code
End Sub

