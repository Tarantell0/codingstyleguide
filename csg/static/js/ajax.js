/*
* Deprecated
*$(document).ready(function(){
*    //$('.user-input').hide();
*    //$('#search').keyup(function(){
*    $('#search').keydown(function (e){
*        if(e.keyCode == 13){
*            $.ajax({
*                type: "GET",
*                url: "/search/",
*                data: { 
*                    'text' : $('#search').val(),
*                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
*                },
*                success: function(data){
*                    window.location.href = "/search/?text=" + $('#search').val()
*                },
*                dataType: 'html'
*            });
*        }
*    });
*
*    $('#input-declaration').keyup(function(){
*        $.ajax({
*            type: "POST",
*            url: "/post/convention/",
*            data: { 
*                'input_text' : $('#input-declaration').val(),
*                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
*            },
*            success: function(){
*                console.log('success');
*            },
*            dataType: 'html'
*        });
*    });
*    
*    *
*     *  Autocomplete Programming Tag on AddNamingConvention 
*     *  version 1.1
*     *
*     $('#id_language_tag').keyup(function(){
*         $.ajax({
*             type: 'POST',
*             url: '/tag_finder/',
*             data: {
*                 'tag_typed': $('#id_language_tag').val(),
*                 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
*             },
*             success: function(data, textStatus, jqXHR){
*                 console.log('data: '+ data);
*                 $('#id_language_tag').attr('placeholder', data);
*                 //$('#id_language_tag').autocomplete({source:data});
*             },
*             dataType: 'html'
*
*         });
*     });
*     *
*});
*
*function searchSuccess(data, textStatus, jqXHR)
*{
*    $('#search-results').html(data);
*}
*/
