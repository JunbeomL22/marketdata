Option Explicit

Sub LoadETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim python_code as String
    Dim file_name as String
    Dim output_head as String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value
    output_head = ws.Range("C6").Value
    ' erase the 1000 rows and 30 columns from output_head 
    ws.Range(output_head).Resize(1000, 30).ClearContents

    python_code = "import base_data;"
    python_code = python_code & "base_data.load_infomax_etf_base_data("
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"

    RunPython python_code
End Sub

Sub SaveETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name as String
    Dim retrieval_date as String
    Dim parameter_date as String
    Dim python_code as String
    Dim file_name as String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value

    python_code = "import base_data;"
    python_code = python_code & "base_data.save_infomax_etf_base_data("
    python_code = python_code & "retrieval_date='" & retrieval_date & "',"
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "')"

    RunPython python_code
End Sub

Sub LoadList()
    Dim ws As Worksheet
    Dim sheet_name as String
    Dim python_code as String
    Dim dt as String
    Dim market as String
    Dim type_name as String
    Dim rank as String
    Dim start_date as String
    Dim end_date as String
    Dim investor as String
    Dim num_code as String
    Dim num_page as String
    Dim base_file_date as String
    Dim file_name as String
    Dim output_head as String

    sheet_name = "List"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    dt = ws.Range("C5").Value
    market = ws.Range("C6").Value
    type_name = ws.Range("C7").Value
    rank = ws.Range("C8").Value
    start_date = ws.Range("C9").Value
    end_date = ws.Range("C10").Value
    investor = ws.Range("C11").Value
    num_code = ws.Range("C12").Value
    num_page = ws.Range("C13").Value
    base_file_date = ws.Range("C14").Value
    file_name = ws.Range("C15").Value
    output_head = ws.Range("C16").Value

    If market = "전체" Then
        market = ""
    ElseIf market = "거래소" Then
        market = "1"
    ElseIf market = "거래소 기타" Then
        market = "2"
    ElseIf market = "KRX" Then
        market = "5"
    ElseIf market = "코스닥" Then
        market = "7"
    ElseIf market = "코스닥 기타" Then
        market = "8"
    End If    
    
    If rank = "거래대금" Then   
        rank = "trading"
    ElseIf rank = "시가총액" Then
        rank = "cap"
    ElseIf rank = "등락률" Then
        rank = "rate"
    End If

    python_code = "import infomax_base_data;"
    python_code = python_code & "infomax_base_data.load_list("
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "date='" & dt & "',"
    python_code = python_code & "market='" & market & "',"
    python_code = python_code & "type_name='" & type_name & "',"
    python_code = python_code & "rank='" & rank & "',"
    python_code = python_code & "start_date='" & start_date & "',"
    python_code = python_code & "end_date='" & end_date & "',"
    python_code = python_code & "investor='" & investor & "',"
    python_code = python_code & "num_code=" & num_code & ","
    python_code = python_code & "num_page=" & num_page & ","
    python_code = python_code & "base_file_date='" & base_file_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"

    RunPython python_code
End Sub