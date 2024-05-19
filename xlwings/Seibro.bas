Attribute VB_Name = "Seibro"
Option Explicit

Public Sub SaveSeibroDividend()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim start_date As String
    Dim end_date As String
    Dim etf_dividend_type As String
    Dim sleep_time As String
    Dim file_name As String
    Dim python_code As String

    sheet_name = "Dividend"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("C4").Value
    retrieval_date = ws.Range("C5").Value
    start_date = ws.Range("C6").Value
    end_date = ws.Range("C7").Value
    etf_dividend_type = ws.Range("C8").Value
    sleep_time = ws.Range("C9").Value
    file_name = ws.Range("C10").Value

    python_code = "import seibro_io; seibro_io.save_seibro_dividend("
    python_code = python_code & "parameter_date=" & "'" & parameter_date & "', "
    python_code = python_code & "retrieval_date=" & "'" & retrieval_date & "', "
    python_code = python_code & "start_date=" & "'" & start_date & "', "
    python_code = python_code & "end_date=" & "'" & end_date & "', "
    python_code = python_code & "etf_dividend_type=" & "'" & etf_dividend_type & "', "
    python_code = python_code & "sleep_time=" & "'" & sleep_time & "', "
    python_code = python_code & "file_name=" & "'" & file_name & "')"

    RunPython python_code
End Sub

Public Sub LoadSeibroDividend()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Dividend"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C10").Value
    output_head = ws.Range("C11").Value

    python_code = "import seibro_io; seibro_io.load_seibro_dividend("
    python_code = python_code & "sheet_name=" & "'" & sheet_name & "', "
    python_code = python_code & "parameter_date=" & "'" & parameter_date & "', "
    python_code = python_code & "file_name=" & "'" & file_name & "',"
    python_code = python_code & "output_head=" & "'" & output_head & "')"

    RunPython python_code
End Sub


