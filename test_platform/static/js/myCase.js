/**
 * Created by anier on 19/02/2020.
 */

//初始化项目>模块 二级菜单:
var selectInit = function (defaultProjectId,defaultModultId) {
    var cmbProject = document.getElementById("selectProject");
    var cmbModule =  document.getElementById("selectModule");
    var dataList=[];

    //设置默认选项:
    function setDefaultOption(obj,id) {
        for(var i=0; i<obj.options.length; i++){
            if(obj.options[i].value == id){
                obj.selectedIndex = i;
                return;
            }
        }
    }

    //创建下拉选项:
    function addOption(cmb,obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.name;
        option.value = obj.id;
    }

    //改变项目:
    function changeProject() {
        cmbModule.options.length=0;
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        for(let i=0; i<dataList.length; i++){
            if (dataList[i].id == pid){
                let modules = dataList[i].moduleList;
                console.log("对应模块列表",pid)
                for(let j=0;j<modules.length; j++){
                    addOption(cmbModule,modules[j]);
                }
            }
        }
        setDefaultOption(cmbModule,defaultModultId);
    }

    function getSelectData() {
        //调用select数据列表
        $.get("/testcase/get_select_data",{},function (resp) {
            if(resp.status === 10200) {
                dataList = resp.data;
                console.log("想要的数据格式:",dataList)
                //遍历项目:
                for (var i = 0; i < dataList.length; i++) {
                    addOption(cmbProject, dataList[i]);
                     console.log("得到的项目数据:",dataList)
                }
                setDefaultOption(cmbProject,defaultProjectId);
                changeProject();
                cmbProject.onchange = changeProject;
            }
             setDefaultOption(cmbProject,defaultProjectId);


        });
    }
    //调用getSelectData函数
    getSelectData();
};



 //获取用例:
 var TestCaseInit = function () {
     var url= document.location;
     var cid=url.pathname.split("/")[3];

       $.post("/testcase/get_case_info",
        {
            cid: cid,
        },
     function (resp,status){
        console.log("返回的结果",resp.data)
        document.querySelector("#req_url").value = resp.data.url;
        //请求方法
        if(resp.data.method == 1){
            document.querySelector("#get").setAttribute("checked","");
        }
        else if(resp.data.method == 2){
            document.querySelector("#post").setAttribute("checked","");
        }
        //headers
         document.querySelector("#header").value = resp.data.header;

        //参数类型:
        if(resp.data.parameter_type == 1){
            document.querySelector("#form_data").setAttribute("checked","");
        }
        else if(resp.data.parameter_type == 2){
            document.querySelector("#json_data").setAttribute("checked","");
        }
         //parameter_body
         document.querySelector("#parameter").value = resp.data.parameter_body;
        //断言的类型:
        if(resp.data.assert_type == 1){
           document.querySelector("#contains").setAttribute("checked","");
        }
        else if(resp.data.assert_type == 2){
            document.querySelector("#matches").setAttribute("checked","");
        }
        // 断言的值:
         document.querySelector("#assert").value = resp.data.assert_body;

        //用例名称:
          document.querySelector("#case_name").value = resp.data.name;

        // 初始化菜单
         selectInit(resp.data.project_id,resp.data.module_id)

   });
 }