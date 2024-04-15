Option Explicit

Public Sub LoadEtfPdf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim output_range_name As String
    Dim date_cell As String
    Dim base_info_file_cell as String
    Dim pdf_file_cell as String
    Dim source_cell as String
    Dim match_file_name_cell As String
    Dim code As String

    sheet_name = "EtfPdf"
    output_range_name = "EtfPdf"
    date_cell = "C4"
    base_info_file_cell = "C5"
    pdf_file_cell = "C6"
    source_cell = "C7"

    Set this_sht = Sheets(sheet_name)
    code = "import load_etf_pdf;"
    code = code + "load_etf_pdf.load_etf_pdf(sheet_name = '" & sheet_name & "', "
    code = code + "output_range_name = '" & output_range_name & "', "
    code = code + "date_cell = '" & date_cell & "', "
    code = code + "base_info_file_cell = '" & base_info_file_cell & "', "
    code = code + "pdf_file_cell = '" & pdf_file_cell & "', "
    code = code + "source_cell = '" & source_cell & "')"

    RunPython code

End Sub

Public Sub SaveEtfPdf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim base_info_file as String
    Dim pdf_file As String
    Dim code As String

    sheet_name = "EtfPdf"
    Set this_sht = Sheets(sheet_name)

    base_info_file = this_sht.Range("C5").Value
    pdf_file = this_sht.Range("C6").Value

    code = "import load_etf_pdf;"
    code = code + "load_etf_pdf.save_etf_pdf(base_info_file = '" & base_info_file & "', "
    code = code + "pdf_file = '" & pdf_file & "')"

    RunPython code
End Sub
