var frame_count = 1;

function close_info() {
  document.getElementById("alert_info").style.visibility = "hidden";
}

function close_err() {
  document.getElementById("alert_error").style.visibility = "hidden";
}

function on() {
  document.getElementById("overlay").style.display = "block";
}

function off() {
  document.getElementById("overlay").style.display = "none";
}

var body = $("body");
body.on("click", "button.add-row", function () {
  var table = $(this).closest("div.table-content"),
    tbody = table.find("tbody"),
    thead = table.find("thead");

  if (tbody.children().length > 0) {
    tbody.find("tr:last-child").clone().appendTo(tbody);
  } else {
    var trBasic = $("<tr />", {
        html: '<td><span class="remove remove-row">x</span></td><td><input type="text" class="form-control" /></td>',
      }),
      columns = thead.find("tr:last-child").children().length;

    for (
      var i = 0, stopWhen = columns - trBasic.children.length;
      i < stopWhen;
      i++
    ) {
      $("<td />", { text: "static element" }).appendTo(trBasic);
    }
    tbody.append(trBasic);
  }
});

body.on("click", "span.remove-row", function () {
  $(this).closest("tr").remove();
});

body.on("click", "span.remove-col", function () {
  var cell = $(this).closest("th"),
    index = cell.index() + 1;
  cell
    .closest("table")
    .find("th, td")
    .filter(":nth-child(" + index + ")")
    .remove();
});

$(document).ready(function () {
  $("body").append($('<script src="static/js/md5.min.js"></script>'));
  $("body").append(
    $('<script type=module defer src="static/js/jquery-3.4.1.min.js"></script>')
  );
});

function add_row(elem) {
  var row_index = elem.parentElement.parentElement.children[0].rows.length - 1;
  var row = elem.parentElement.parentElement.children[0].rows[row_index];
  var table = elem.parentElement.parentElement.children[0];
  var clone = row.cloneNode(true);
  var cells_length = clone.cells.length - 1;
  for (var i = 1; i < cells_length; i++) {
    clone.cells[i].children[0].value = "";
  }
  table.appendChild(clone);
}

function delete_row(elem) {
  if (elem.parentElement.parentElement.parentElement.rows.length > 2) {
    elem.parentElement.parentElement.remove();
  } else {
    alert("First row can not be deleted!");
  }
}

function add_users() {
  code_table = document.getElementsByClassName("code_table")[0];
  code_rows = code_table.rows;

  for (var j = 1; j < code_rows.length; j++) {
    tds = code_rows[j].children;

    if (tds[0].firstElementChild.value == "") {
      alert("Role cannot be blank in row : " + j);
      return;
    }

    if (tds[1].firstElementChild.value == "") {
      alert("First Name cannot be blank in row : " + j);
      return;
    }

    if (tds[2].firstElementChild.value == "") {
      alert("Last Name cannot be blank in row : " + j);
      return;
    }

    if (tds[3].firstElementChild.value == "") {
      alert("Password cannot be blank in row : " + j);
      return;
    }

    if (tds[4].firstElementChild.value == "") {
      alert("Email cannot be blank in row : " + j);
      return;
    }
  }
  var final_table_data = {};
  var full_data = {};
  for (var j = 1; j < code_rows.length; j++) {
    tds = code_rows[j].children;
    var table_data = {};
    table_data["Role"] = tds[0].firstElementChild.value;
    table_data["fname"] = tds[1].firstElementChild.value;
    table_data["lname"] = tds[2].firstElementChild.value;
    salted_pass = tds[3].firstElementChild.value;
    table_data["email"] = tds[4].firstElementChild.value;
    encrypted_pass = md5(salted_pass);
    table_data["Password"] = encrypted_pass;
    final_table_data[j] = table_data;
  }

  full_data["observation"] = final_table_data;
  $.getJSON(
    "/submit_add_user",
    {
      params_data: JSON.stringify(full_data),
    },
    function (result) {
      alert("Users Added kindly note down usernam-" + result.userID);
    }
  );
}

function view_user_details() {
  USERNAME = $("#USERNAME").val();
  if ($("#USERNAME").val() == "") {
    alert("PLEASE SELECT USERNAME");
    return;
  }
  basic_details = {};
  basic_details["USERNAME"] = $("#USERNAME").val();
  $.getJSON(
    "/get_user_detail_by_userID_sheet",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      var record_list = result["user_list"][0];
      $("#USERTABLE").empty();
      var header =
        "<tr>\
				 <th>Role</th><th>Company Name</th><th>Username</th><th>First Name</th>\
				 <th>Last Name</th><th>Email ID</th><th>Status</th></tr>";
      $("#USERTABLE").append(header);

      var temp =
        '<tr id="myTableRow" name="myTableRow">\
		<td><select class="text-field" name="ROLE" id="ROLE" style="width:100%">';

      if (record_list.ROLE == "admin") {
        temp = temp + '<option value="admin" selected>Admin</option>';
        temp = temp + '<option value="analyst" >Service</option>';
        temp = temp + "</select></td>";
      }
      if (record_list.ROLE == "analyst") {
        temp = temp + '<option value="admin" >Admin</option>';
        temp = temp + '<option value="analyst" selected >Service</option>';
        temp = temp + "</select></td>";
      }

      temp =
        temp +
        '<td><input type="text" name="Username" id="Username" value=' +
        record_list.USERNAME +
        ' class="text-field" disabled></td>\
		<td><input type="text" name="FirstNAME" id="FirstNAME" value=' +
        record_list.FNAME +
        ' class="text-field" ></td>\
		<td><input type="text" name="LastNAME" id="LastNAME" value=' +
        record_list.LNAME +
        ' class="text-field" ></td>\
		<td><input type="text" name="emaild" id="emaild" value=' +
        record_list.EMAILID +
        ' class="text-field" ></td>\
		<td>\
		<select class="text-field" name="STATUS" id="STATUS" style="width:100%">\
		';
      if (record_list.STATUS == "ACTIVE") {
        temp = temp + '<option value="ACTIVE" selected>ACTIVE</option>';
        temp = temp + '<option value="INACTIVE" >INACTIVE</option>';
      } else {
        temp = temp + '<option value="ACTIVE" >ACTIVE</option>';
        temp = temp + '<option value="INACTIVE" selected>INACTIVE</option>';
      }

      temp = temp + "</select></td></tr>";
      $("#USERTABLE tr:last").after(temp);
    }
  );
}

function delete_user_details() {
  USERNAME = $("#USERNAME").val();
  if ($("#USERNAME").val() == "") {
    alert("PLEASE SELECT USERNAME");
    return;
  }
  basic_details = {};
  basic_details["USERNAME"] = $("#USERNAME").val();
  $.getJSON(
    "/delete_user",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      alert(result.error);
    }
  );
}

function update_user_details() {
  if ($("#USERNAME").val() == "") {
    alert("PLEASE SELECT USERNAME");
    return;
  }

  if ($("#FirstNAME").val() == "") {
    alert("Please Enter First Name");
    return;
  }
  if ($("#LastNAME").val() == "") {
    alert("Please Enter Last Name");
    return;
  }
  if ($("#emaild").val() == "") {
    alert("Please Enter Email id");
    return;
  }
  basic_details = {};
  basic_details["USERNAME"] = $("#USERNAME").val();
  basic_details["FirstNAME"] = $("#FirstNAME").val();
  basic_details["LastNAME"] = $("#LastNAME").val();
  basic_details["STATUS"] = $("#STATUS").val();
  basic_details["ROLE"] = $("#ROLE").val();
  basic_details["emaild"] = $("#emaild").val();
  basic_details["PASSWORD"] = "";
  $.getJSON(
    "/submit_update_user_details",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      alert("User Details Updated");
    }
  );
}

function update_profile_details() {
  if ($("#FNAME").val() == "") {
    alert("Please Enter First Name");
    return;
  }
  if ($("#LNAME").val() == "") {
    alert("Please Enter Last Name");
    return;
  }
  if ($("#emaild").val() == "") {
    alert("Please Enter Email id");
    return;
  }
  if ($("#PASSWORD").val() == "") {
    alert("Please Enter PASSWORD");
    return;
  }
  basic_details = {};
  basic_details["USERNAME"] = $("#USERNAME").val();
  basic_details["FirstNAME"] = $("#FNAME").val();
  basic_details["LastNAME"] = $("#LNAME").val();
  salted_pass = $("#PASSWORD").val();
  encrypted_pass = md5(salted_pass);
  basic_details["PASSWORD"] = encrypted_pass;
  basic_details["emaild"] = $("#EMAILID").val();
  $.getJSON(
    "/submit_update_user_details",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      alert("User Details Updated");
    }
  );
}

function updateProductList() {
  code_table = document.getElementsByClassName("code_table")[0];
  code_rows = code_table.rows;
  var final_table_data = {};
  var full_data = {};
  for (var j = 1; j < code_rows.length; j++) {
    tds = code_rows[j].children;
    var table_data = {};
    table_data["Product_Name"] = tds[0].firstElementChild.value;
    table_data["Generic_Name"] = tds[1].firstElementChild.value;
    table_data["Form"] = tds[2].firstElementChild.value;
    table_data["API_with_strength"] = tds[3].firstElementChild.value;
    table_data["Minimum_Batch_size_NOS"] = tds[4].firstElementChild.value;
    table_data["Minimum_Batch_size_MG"] = tds[5].firstElementChild.value;
    table_data["MRDD"] = tds[6].firstElementChild.value;
    table_data["LRDD_MG"] = tds[7].firstElementChild.value;
    table_data["LRDD_NOS"] = tds[8].firstElementChild.value;
    table_data["PDE_VALUE"] = tds[9].firstElementChild.value;
    table_data["LD50"] = tds[10].firstElementChild.value;
    table_data["NOEL"] = tds[11].firstElementChild.value;
    final_table_data[j] = table_data;
  }

  full_data["observation"] = final_table_data;

  on();
  $.getJSON(
    "/submit_UpdateProductList",
    {
      params_data: JSON.stringify(full_data),
    },
    function (result) {
      off();
      alert("Product List Updated");
    }
  );
}

function submit_Report() {
  var data = Array();
  code_table = document.getElementsByClassName("code_table")[0];
  var header_length = code_table.rows[0].children.length;
  code_rows = code_table.rows;
  for (var i = 0; i < code_rows.length; i++) {
    tds = code_rows[i].children;
    data[i] = Array();
    for (var j = 1; j < header_length; j++) {
      if (i == 0 && j == 1) {
        data[i][j] = "Equipment";
      } else if (i == 0 && j > 1) {
        data[i][j] =
          code_rows[i].children[j].children[0].firstElementChild.value;
      } else {
        data[i][j] = tds[j].firstElementChild.value;
      }
    }
  }
  on();
  $.getJSON(
    "/submit_cleaning_room_report",
    {
      params_data: JSON.stringify(data),
    },
    function (result) {
      off();
      var link = document.createElement("a");
      link.href = result.file_path;
      link.download = result.file_name;
      link.dispatchEvent(new MouseEvent("click"));
    }
  );
}

function view_report_log() {
  basic_details = {};
  basic_details["USERNAME"] = $("#USERNAME").val();
  basic_details["startdate"] = $("#startdate").val();
  basic_details["enddate"] = $("#enddate").val();
  $("#ReportTable").empty();
  $("#DownlodReportbtn").hide();
  on();
  $.getJSON(
    "/view_reportlog",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      report_list = result["report_log"];
      var header = "<th>User Name</th><th>Report Name</th><th>DOWNLOAD</th>";
      $("#ReportTable").append(header);
      for (var j = 0; j < report_list.length; j++) {
        var prepared_by = report_list[j].prepared_by;
        var report_number = report_list[j].report_number;

        var blob = new Blob([s2ab(atob(report_list[j].data))], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,",
        });
        var link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);

        prepared_by = prepared_by.split(" ").join("\xa0");
        report_number = report_number.split(" ").join("\xa0");

        var temp =
          '<tr>\
			<td><input type="text" name="prepared_by" value=' +
          prepared_by +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="report_number" value=' +
          report_number +
          ' class="text-field" disabled></td>\
			<td><a href=' +
          link +
          " download=" +
          report_list[j].file_name +
          ">" +
          report_list[j].file_name +
          "</a><td></tr>";
        $("#ReportTable").append(temp);
        $("#DownlodReportbtn").show();
        off();
      }
    }
  );
}

function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
}

function DownlodReport() {
  var table = document.getElementById("ReportTable");
  for (var i = 0; i < table.rows.length + 1; i++) {
    table.rows[i].cells[2].children[0].click();
  }
}
function edit_report(version_number) {
  basic_details = {};
  basic_details["version_number"] = version_number;
  $.getJSON(
    "/getProductData",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      report_list = result["product_log"];
      var header =
        "<th>Product Name</th>\
		<th>Generic Name</th>\
		<th>Form</th>\
		<th>API with strength</th>\
		<th>Minimum Batch size NOS</th>\
		<th>Minimum Batch size MG</th>\
		<th>MRDD</th>\
		<th>LRDD MG</th>\
		<th>LRDD NOS</th>\
		<th>PDE VALUE</th>\
		<th>LD50</th>\
		<th>NOEL</th>";
      $("#ReportTable").empty();
      $("#ReportTable").append(header);
      for (var j = 0; j < report_list.length; j++) {
        var temp =
          '<tr>\
			<td><input type="text" name="Product_Name" value=' +
          report_list[j].Product_Name +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Generic_Name" value=' +
          report_list[j].Generic_Name +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Form" value=' +
          report_list[j].Form +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="API_with_strength" value=' +
          report_list[j].API_with_strength +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Minimum_Batch_size_NOS" value=' +
          report_list[j].Minimum_Batch_size_NOS +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Minimum_Batch_size_MG" value=' +
          report_list[j].Minimum_Batch_size_MG +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="MRDD" value=' +
          report_list[j].MRDD +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="LRDD_MG" value=' +
          report_list[j].LRDD_MG +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="LRDD_NOS" value=' +
          report_list[j].LRDD_NOS +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="PDE_VALUE" value=' +
          report_list[j].PDE_VALUE +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="LD50" value=' +
          report_list[j].LD50 +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="NOEL" value=' +
          report_list[j].NOEL +
          ' class="text-field" disabled></td>\
			';
        $("#ReportTable").append(temp);
        $("#DownlodReportbtn").show();
      }
    }
  );
}

function view_logbook() {
  if ($("#startdate").val() == "") {
    alert("Please select Start Date");
    return;
  }
  if ($("#enddate").val() == "") {
    alert("Please select End Date");
    return;
  }

  basic_details = {};
  basic_details["user_id"] = $("#user_id").val();
  basic_details["STATUS"] = $("#STATUS").val();
  basic_details["startdate"] = $("#startdate").val();
  basic_details["enddate"] = $("#enddate").val();

  $.getJSON(
    "/get_elogbook",
    {
      params_data: JSON.stringify(basic_details),
    },
    function (result) {
      record_list = result["elog_list"];

      $("#LOGTABLE").empty();

      var header =
        "<tr><th>Version</th><th>Status</th><th>Updated By</th><th>View Data</tr>";

      $("#LOGTABLE").append(header);
      for (var j = 0; j < record_list.length; j++) {
        var temp =
          '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="Version" value=' +
          record_list[j].VERSION +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Status" value=' +
          record_list[j].STATUS +
          ' class="text-field" disabled></td>\
			<td><input type="text" name="Updated_By" value=' +
          record_list[j].UPDATED_BY +
          ' class="text-field" disabled></td>\
			<td><button style="background-color:#ffcc00" class="add_user-btn" onclick="edit_report(\'' +
          record_list[j].VERSION +
          "')\" >View Data</button>\
			</td>\
			</tr>";

        $("#LOGTABLE tr:last").after(temp);
      }
    }
  );
}
