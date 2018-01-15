$(function () {
    reloadOnekey();
    checkOnekeyLogin();

    $('.getcode').on('click',
        function () {
            var time = 0;
            $.post("/getkey",
                function (data) {
                    $('.getcode').hide();
                    $('#code').html(data);
                    time = $('#time').text().split(':')[1];

                    var secs = time;
                    for (var i = 1; i <= secs; i++) {
                        window.setTimeout(' if(' + i + ' == ' + secs + ') {' +
                            '$(".getcode").trigger("click");' +
                            ' }' +
                            ' else {' +
                            ' var printnr = ' + secs + '-' + i + ';' +
                            ' $("#time").text("Time:"+printnr);' +
                            '$("#progress_bar .ui-progress").animateProgress(' + (1 - (i / secs)) * 100 + ',function(){});' +
                            '}', i * 1000);
                    }
                    //timename=setTimeout('$(".getcode").trigger("click"); ',time*1000);

                });
        });
});
var t1;
var reload;


function reloadOnekey() {
    $('.onekeyauth').off();
    t1 = window.setInterval(checkOnekeyLogin, 5000);
}
function checkOnekeyLogin() {
    $.get("/getOnekey",
        function (data) {
            //data = '{"callback_url": "https://www.battlenet.com.cn/login/authenticator/pba","session": {"request_id": "5DRQ","time_created_millis": 1506326878852,"ip_address": "123.118.22.142","application": "COM_ROOT","country": "中国","device_type": "OTHER","two_factor_state": "PENDING","action_type": "LOGIN","expiration_time_millis": 1506326998852},"login_message_template": "新的请求 {request_id} {message}","message": "从中国通过暴雪游戏网站发送"}';
            if (data.length == 0) {
                $('#logininfo').html("<p>没有登录请求</p>");
                window.clearInterval(reload);
                return
            }
            var jdata = eval("(" + data + ")");
            id = jdata.session.request_id;
            $('#logininfo').html("<ul class=\"actions vertical\"><li><p class='reqid'>请求ID:" + id + "</p></li><li><p><a class='button big wide smooth-scroll-middle onekeyauth'>确认</a></p></li></ul>");

            $('.onekeyauth').on('click',
                function () {
                    var id = $('.reqid').html().split(':')[1];
                    $.get("/AcceptBattleNetLogin", { requestId: id }, function () {
                        $('#logininfo').html("<p>已确认</p>")
                    });
                    reload = window.setTimeout(reloadOnekey, 5000);
                });
            window.clearInterval(t1);
            reload = window.setTimeout(reloadOnekey, 30000);
        });

}

