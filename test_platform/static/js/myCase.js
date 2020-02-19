/**
 * Created by anier on 19/02/2020.
 */
var ProjectInit = function (_cmdProject) {
    var cmbProject = document.getElementById(_cmdProject);
    var options = "";

    function cmbAddOption(cmb, project_obj) {
        console.log(project_obj);
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = project_obj.name;
        option.value = project_obj.id;
    }

    function getProjectListInfo() {
        $.get("/project/get_project_list/", {}, function (resp) {
            if (resp.status === 10200) {
                console.log(resp.data);
                let dataList = resp.data;
                for (var i = 0; i < dataList.length; i++) {
                    cmbAddOption(cmbProject, dataList[i]);
                }
                // cmbSelect(cmbProject, defaultProject);
            }else {
                window.alert(resp.message);
            }
        });

    }

    getProjectListInfo()
};