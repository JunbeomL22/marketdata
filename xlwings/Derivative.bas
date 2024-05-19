Attribute VB_Name = "Derivative"
Option Explicit

Sub SaveDerivativesBaseData()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim sheet_name As String
    Dim start_date As String
    Dim end_date As String
    Dim drop_spread As String
    Dim file_name As String
    Dim python_code As String

    sheet_name = "DerivativesBase"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("G2").Value
    start_date = ws.Range("G3").Value
    end_date = ws.Range("G4").Value
    If ws.Range("G5").Value = "Y" Then
        drop_spread = "True"
    Else
        drop_spread = "False"
    End If
    
    file_name = ws.Range("G6").Value

    python_code = "import krx_derivatives;"
    python_code = python_code & "krx_derivatives.save_derivatives_base_data("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "start_date='" & start_date & "',"
    python_code = python_code & "end_date='" & end_date & "',"
    python_code = python_code & "drop_spread=" & drop_spread & ","
    python_code = python_code & "file_name='" & file_name & "')"

    RunPython python_code
End Sub

Sub LoadDerivativesBaseData()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim output_head As String
    Dim file_name As String
    Dim python_code As String
    Dim drop_option As String

    sheet_name = "DerivativesBase"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("G2").Value
    file_name = ws.Range("G6").Value
    drop_option = ws.Range("G7").Value
    output_head = ws.Range("G8").Value
    'erase the 1000 rows and 30 columns from output_head
    ws.Range(output_head).Resize(5000, 30).ClearContents

    python_code = "import krx_derivatives;"
    python_code = python_code & "krx_derivatives.load_derivatives_base_data("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"
    
    RunPython python_code
End Sub

Public Sub SaveBbgTickerForDividend()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim deriv_und_file As String
    Dim output_file_name As String
    Dim python_code As String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("C2").Value
    deriv_und_file = ws.Range("C10").Value
    output_file_name = ws.Range("C15").Value    

    python_code = "import infomax_io; infomax_io.save_bbg_tickers_for_dividend("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "deriv_und_file='" & deriv_und_file & "',"
    python_code = python_code & "output_file_name='" & output_file_name & "')"

    RunPython python_code
End Sub