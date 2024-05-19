Attribute VB_Name = "FindEtf"
Option Explicit

Public Sub FindEtf()
    Dim this_sht As Worksheet
    Dim sheet_name As String
    Dim codes As String
    Dim all_futures As String
    Dim dt As String
    Dim pdf_file As String
    Dim output_head As String

    sheet_name = "FindETF"
    Set this_sht = Sheets(sheet_name)
    codes = this_sht.Range("C3").Value
    all_futures = this_sht.Range("C4").Value
    dt = this_sht.Range("C5").Value
    
    pdf_file = this_sht.Range("C6").Value
    output_head = this_sht.Range("C7").Value
    'clear from output_head to 15 columns, 200 rows
    this_sht.Range(output_head).Resize(200, 3).ClearContents

    Dim python_code As String
    
    python_code = "import find_etf;"
    python_code = python_code + "find_etf.find_etf(codes = '" & codes & "', "
    python_code = python_code + "all_futures = '" & all_futures & "', "
    python_code = python_code + "dt = '" & dt & "', "
    python_code = python_code + "sheet_name = '" & sheet_name & "', "
    python_code = python_code + "pdf_file = '" & pdf_file & "', "
    python_code = python_code + "output_head = '" & output_head & "')"

    RunPython python_code
End Sub
