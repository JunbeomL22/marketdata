Option Explicit

Public Sub LoadEtfPdf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim output_range_name As String
    Dim date_cell As String
    Dim match_file_name_cell As String
    Dim code As String

    sheet_name = "EtfPdf"
    output_range_name = "EtfPdf"
    date_cell = "C4"
    match_file_name_cell = "C5"

    Set this_sht = Sheets(sheet_name)
    code = "import load_etfpdf;"
    code = code + "load_etfpdf.load_etfpdf(sheet_name = '" & sheet_name & "', "
    code = code + "output_range_name = '" & output_range_name & "', "
    code = code + "date_cell = '" & date_cell & "', "
    code = code + "match_file_name_cell = '" & match_file_name_cell & "')"

    RunPython code

End Sub
