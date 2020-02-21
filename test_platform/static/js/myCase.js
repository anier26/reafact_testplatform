/**
 * Created by anier on 19/02/2020.
 */

function cmbAddOption(cmb, obj) {
    let option = document.createElement("option");
    cmb.options.add(option);
    option.innerHTML = obj.name;
    option.value = obj.id;
}

//清除下拉选项
function clearOPtion(cmb){
    for(let i=0; i <= cmb.length; i++){
        cmb.options.remove(cmb[i])
    }
}

var ProjectInit = function (_cmdProject) {
    var cmbProject = document.getElementById(_cmdProject);
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

//获取某一个项目的模块列表
 var ModelInit = function (_cmbModel,pid){
    var cmbModel = document.getElementById(_cmbModel);
    function getModelListInfo() {
         $.post("/model/get_model_list/", {"pid":pid
            }, function (resp) {
                if (resp.status === 10800) {
                    console.log(resp.data);
                    let dataList = resp.data;
                    clearOPtion(cmbModel);
                    for (let i = 0; i < dataList.length; i++) {
                         cmbAddOption(cmbModel, dataList[i]);
                    }
                     $('#model_name').selectpicker('refresh')
                }else {
                    window.alert(resp.message);
                }
            }
         )
    }
    getModelListInfo();
};