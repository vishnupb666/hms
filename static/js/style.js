$(document).ready(function(){
    $('.nav-link').click(function(e){
        $('.nav-link').removeClass('active');
        
        var $this = $(this);
        if(!$this.hasClass('active')){
            $this.addClass('active');
            
        }
       
  })

  toastr.options = {
    toastClass: 'alert',
    iconClasses: {
        error: 'alert-error',
        info: 'alert-info',
        success: 'alert-success',
        warning: 'alert-warning'
    }
}
    
})

function profile(){
        url = '/profile';
        $.ajax({
            url : url,
            beforeSend:function(){
                $('#section_div').empty()
            },
            success:function(result){
                $('#section_div').html(result) 
                console.log(result)  
                
            },
            
        });

}



function openNav() {
        if(!$('.nav-link').hasClass('nav_hide left_side_hide'))
        {
                
        document.getElementById("mySidebar").style.width = "5%";
        document.getElementById("main").style.width = "95%";
        $(".nav-link span").animate({opacity: "0"});
       
        $('.sideNav').css('display','none')
        $('.pnav').css('display','none')
        $('.pt_nav').css('display','none')
        $('.Anav').css('display','none')
        $('.a_c_nav').css('display','none')
        $('.a_d_nav').css('display','none')
        $('.vpnav').css('display','none')
        $('.nav-link').addClass('nav_hide left_side_hide')
        }
        else{
            closeNav()
        }
        
  }

function closeNav() {

    document.getElementById("mySidebar").style.width = "20%";
    document.getElementById("main").style.width = "80%";
    $(".nav-link span").animate({opacity: "1"});
    $('.sideNav').css('display','block')
    $('.pnav').css('display','block')
    $('.pt_nav').css('display','block')
    $('.Anav').css('display','block')
    $('.a_c_nav').css('display','block')
    $('.a_d_nav').css('display','block')
    $('.vpnav').css('display','block')
    
    $('.nav-link').removeClass('nav_hide left_side_hide')
    
   
  }

function TakeAppointment(){

    url = '/takeAppointment';
        $.ajax({
            url : url,
            beforeSend:function(){
                $('#section_div').empty()
            },
            success:function(result){
                $('#section_div').html(result) 
                console.log(result)  
                
            },
            
        });

}

function viewPatients(){

    url = '/viewPatients';
    $.ajax({
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(result){
            $('#section_div').html(result) 
            console.log(result)  
            
        },
        
    });

}
function viewAppointment(){

    url = '/viewAppointment';
    $.ajax({
        url : url,
        beforeSend:function(){
            $('.listAppointments').empty()
        },
        success:function(result){
            $('.listAppointments').html(result) 
            console.log(result)  
            
        },
        
    });

}

// function register() { 
    
//     var data = new FormData($('#register').get(0));
    
//     $.ajax({
//         url: '/sign_in', // same url 'action' in form
//         type: 'POST',
//         data: data,
//         contentType: 'multipart/form-data',
//         processData: false,
//         contentType: false,
//         success: function(data) {
//            if(data.status==1){
//             toastr.success('successfully registered....')
//            }
              
//         }
//     });
    
// }


function generatePassword(){

    url = '/generateOTP';
    $.ajax({
        
        url : url,
        
        beforeSend:function(){
            
        },
        success:function(data){
            
            console.log(data.status)  
            $('#password').val(data.status)
            $('#c_password').val(data.status)
            
        },
        
    });


}

function department(){

    url = '/department_view';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
            
        },
        
    });

}
function addDepartment(){

    var name = $('#dpt_name').val()
    if(name==''){
        toastr.warning('Please eneter department name')
        return
    }
    var data = new FormData($('#add_depart').get(0));
    url = '/addDepartment';
    
    
    $.ajax({
        type:'POST',
        url : url,
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        beforeSend:function(){
           
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully added')
                listdepartment()
            }
            else{
                toastr.warning('something went wrong')
            }
            
        },
        
    });

}

function listdepartment(){
    url = '/listDpartment';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('.list_category').empty()
        },
        success:function(data){
            $('.list_category').html(data)
        },
        
    });

}
function doctors(){
    url = '/doctors';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });

}

function saveDoctor(){

    var data = new FormData($('#doctor_data').get(0));
    url = '/saveDoctor';
    
    
    $.ajax({
        type:'POST',
        url : url,
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        beforeSend:function(){
           
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully added')
                listDoctors();
            }
            else{
                toastr.warning('something went wrong')
            }
            
        },
        
    });


}

function edit_doc(id,name,dep){
    $('#hidden_id').val(id)
    $('#doctor').val(name)
    $('#depart').val(dep)
}
function Doc_refresh(){
    $('#hidden_id').val('')
    $('#doctor').val('')
    $('#depart').val('')
}

function listDoctors(){

    url = '/listDoctors';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#listDoc').empty()
        },
        success:function(data){
            $('#listDoc').html(data)
        },
        
    });

}

function takeAppointment(id){

    var dep = $('#depart').val()
    if(dep==''){
        toastr.warning('Please select doctor')
        return
    }
    
    var doc_name = $('.doctor_name').val()
    if(doc_name == '' | doc_name== null){
        toastr.warning('Please select doctor')
        return
    }
    var time = $('.time').val()
    if(time==''){
        toastr.warning('please select time')
        return
    }
    var current_date = $('#today').val()
    var ap_date = $('#ap_date_time').val()
    var appointdate = formatDate(ap_date);
    
        if(appointdate < current_date){
            toastr.warning('Please select valid date and time')
            return;
        }
    
    var data = new FormData($('#appoint').get(0));
    url = '/addapointment/'+id;
    
    
    $.ajax({
        type:'POST',
        url : url,
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        beforeSend:function(){
           
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully added')
                viewAppointment()
            }
            else{
                toastr.warning('something went wrong')
            }
            
        },
        
    });



}

function formatDate(date) {
    var date = new Date(date);
    var date = date.getFullYear()+"-"+((date.getMonth()+parseInt(1) > 9) ?  date.getMonth()+parseInt(1) : ('0' + date.getMonth()+parseInt(1)))+"-"+((date.getDate() > 9) ?  date.getDate() : ('0' + date.getDate()))
    return date    
}

function depart_refresh(){

    $('#dpt_name').val('')
    $('#hidden_id').val('')

}
function adviewappointmnt(){

    url = '/adViewAppointment';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });


}

function approve(id){
     
    url = '/approve';
    mydata = { appoint_id:id};

    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('request approved....')
                adviewappointmnt();
            }
        },
        
    });
}

function cancelappointment(id){

    url = '/cancelappointment';
    mydata = { appoint_id:id};

    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('request canceled....')
            }
            adviewappointmnt();
        },
        
    });

}

function cancelapp(id){

    url = '/cancelappointment';
    mydata = { appoint_id:id};

    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('request canceled....')
                viewAppointment()
            }
            
        },
        
    });

}


function getAppId(id){
   $('#exampleModal').modal('show')
   var appionment_id = id;
   $('#update_doc').click(function(){
    var doc_id=$('.doctor_name').val();
    var cat_id = $('.depart').val();
   url = '/updateDoctor';
    mydata = { appionment_id:appionment_id,doc_id:doc_id,cat_id:cat_id};

    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('Doctor changed....')
                $('#exampleModal').modal('hide')
                adviewappointmnt();
                
            }
        },
        complete:function(){
            
        }
        
    });



   });
   


}

function getdoctor(){
    departid = $('.depart').val()
    date = $('#ap_date_time').val()
    if(date==''){
        toastr.warning('Please select appointment date')
        return
    }
    console.log(departid)
    url = '/get_doc';

    mydata = { departid:departid,ap_date:date};

    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            $('.doctor_name').empty()
        },
        success:function(doc){
            console.log(doc)
            $.each(doc,function(key,value){
                console.log(value.length)
                console.log(value)
                for(i=0;i<value.length;i++)
                {
                    $('.doctor_name').append(
                        "<option value='"+value[i].id+"'>"+value[i].first_name+"</option>"
                    )
                }
            })

            
            
            
        },
        
    });



}

function delete_doc(id){
    url = '/delete_doc/'+id;
    

    $.ajax({
        url : url,
        method : "POST",
        
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully deleted... ')
                listDoctors();
            }
            
        },
        
    });


}

function delete_patient(id){
     
    url = '/delete_patient/'+id;
    

    $.ajax({
        url : url,
        method : "POST",
       
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('success fully deleted')
                viewPatients();
            }
        },
        
    });
}
function delete_category(id){
     
    url = '/delete_category/'+id;
    

    $.ajax({
        url : url,
        method : "POST",
       
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('success fully deleted')
                listdepartment();
            }
        },
        
    });
}


function edit_category(id,name){

    $('#dpt_name').val(name)
    $('#hidden_id').val(id)
}


function checkfirstname(){
    first_name = $('#fname').val()
    if(!firstIsUppercase(first_name)){
        toastr.warning('First letter must be capital...')
        $('#fname').val('');
        
    }
    

}

function firstIsUppercase(str) {
    if (typeof str !== 'string' || str.length === 0) {
      return false;
    }
  
    if (str[0].toUpperCase() === str[0]) {
      return true;
    }
  
    return false;
  }

  function checkphonenumber(){
   
    var num = $('#phone').val()
   
    if(num.length > 9){
        toastr.warning('Allow only 10 digits')
        $('#phone').blur()
        return;
    }

    
  }

function addrole(){

    url = '/roles';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
            listrole();
        },
        
    });


}

function saveRole(){

    var name = $('#role_name').val()
    if(name==''){
        toastr.warning('Please eneter name')
        return
    }
    var data = new FormData($('#add_role').get(0));
    url = '/saveRole';
    
    
    $.ajax({
        type:'POST',
        url : url,
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        beforeSend:function(){
           
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully added')
                listrole()
            }
            else{
                toastr.warning('something went wrong')
            }
            
        },
        
    });
}

function listrole(){
    url = '/listRole';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('.list_role').empty()
        },
        success:function(data){
            $('.list_role').html(data)
        },
        
    });
}

function edit_role(id,name){
    $('#role_name').val(name)
    $('#hidden_id').val(id)


}

function assign_role(id){
    $('#roleModal').modal('show')
    $('#update_rol').click(function(){
        var rol_id=$('.rol_name').val();
        var dep_id = $('.depart_ment').val();
       url = '/updaterole';
        mydata = { user_id:id,rol_id:rol_id,dep_id:dep_id}
    
        $.ajax({
            url : url,
            method : "POST",
            data : mydata,
            dataType : "json",
            beforeSend:function(){
                
            },
            success:function(data){
                console.log(data)
                if(data.status==1){
                    toastr.success('Doctor saved....')
                    $('#roleModal').modal('hide');
                    viewPatients();
                }
            },
            complete:function(){
                
            }
            
        });
    
    
    
       });
}

function view_doc_wise_patient(id){

    url = '/view_doc_wise_patient/'+id;
 

    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });
        
   

}

function viewdep(){
    var id = $('.rol_name').val()
    if(id==2){
        $('.department_show').css('display','block')
    }
    else{
        $('.department_show').css('display','none')

    }
}

function view_patient(){

    url = '/view_Patients';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });


}
function applyLeave(){

    url = '/applyLeave';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });


}

function apply_leave(){

    var name = $('#reason').val()
    if(name==''){
        toastr.warning('Please  reason ')
        return
    }
    var data = new FormData($('#leave_form').get(0));
    url = '/leave_apply';
    
    
    $.ajax({
        type:'POST',
        url : url,
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        beforeSend:function(){
           
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('successfully added')
                var id = $('#user_id').val()
                list_leave(id)
            }
            else{
                toastr.warning('something went wrong')
            }
            
        },
        
    });

}

function leaveApplication(){

    url = '/leaveApplications';
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('#section_div').empty()
        },
        success:function(data){
            $('#section_div').html(data)
        },
        
    });



}

function leave_approve(id){
   
     
        url = '/leave_approve';
        mydata = { leave_id:id};
    
        $.ajax({
            url : url,
            method : "POST",
            data : mydata,
            dataType : "json",
            beforeSend:function(){
                
            },
            success:function(data){
                console.log(data)
                if(data.status==1){
                    toastr.success('request approved....')
                    leaveApplication()
                }
                else{
                    toastr.warning('Network error')
                }
            },
            
        });
    

}

function list_leave(id=0){

    url = '/list_leave/'+id;
    $.ajax({
       
        url : url,
        beforeSend:function(){
            $('.list_leave').empty()
        },
        success:function(data){
            $('.list_leave').html(data)
        },
        
    });


}
function cancel_levae(id){

    url = '/cancel_leave';
    mydata = { leave_id:id};
    var user_id = $('#user_id').val()
    $.ajax({
        url : url,
        method : "POST",
        data : mydata,
        dataType : "json",
        beforeSend:function(){
            
        },
        success:function(data){
            console.log(data)
            if(data.status==1){
                toastr.success('request canceled....')
                list_leave(user_id)
            }
            
        },
        
    });


}
