Option Explicit

Public Sub FindEtf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim codes As String
    Dim condition as String
    Dim dt As String
    Dim base_file As String
    Dim pdf_file As String
    Dim output_head As String

    sheet_name = "FindETF"
    set this_sht = Sheets(sheet_name)
    codes = this_sht.Range("C3").Value
    condition = this_sht.Range("C4").Value
    dt = this_sht.Range("C5").Value
    base_file = this_sht.Range("C6").Value
    pdf_file = this_sht.Range("C7").Value
    output_head = this_sht.Range("C8").Value
    'clear from output_head to 15 columns, 200 rows
    this_sht.Range(output_head & ":" & this_sht.Cells(200, 15).Address).ClearContents

    Dim code As String
    code = "import find_etf;"
    code = code + "find_etf.load_etf_include(sheet_name = '" & sheet_name & "', "
    code = code + "codes = '" & codes & "', "
    code = code + "condition = '" & condition & "', "
    code = code + "date = '" & dt & "', "
    code = code + "base_file = '" & base_file & "', "
    code = code + "pdf_file = '" & pdf_file & "', "
    code = code + "output_head = '" & output_head & "')"

    RunPython code
End Sub