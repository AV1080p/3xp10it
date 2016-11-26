from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exp10it import execute_sql_in_db
import os
from exp10it import get_key_value_from_config_file
from exp10it import configIniPath
from exp10it import get_http_domain_from_url
from django.http import StreamingHttpResponse
from exp10it import ModulePath
import sys
sys.path.append(ModulePath + "tools/")
from xPang import get_pang_domains
from xSub import get_sub_domains
from xcdn import Xcdn
from highrisk import single_risk_scan
from sqli import sqli_scan
from xdir import single_dirb_scan
from xcms import single_cms_scan
from xwebshell import crack_webshell
from xadmin import crack_admin_login_url
from xwaf import Program as Xwaf
from exp10it import get_target_table_name_list
from exp10it import exist_table_in_db

db_name = eval(get_key_value_from_config_file(configIniPath, "default", 'db_name'))
targets_table_name = eval(get_key_value_from_config_file(configIniPath, "default", 'targets_table_name'))
first_targets_table_name = eval(get_key_value_from_config_file(
    configIniPath, "default", 'first_targets_table_name'))


@login_required
def result(request):
    return render_to_response("result.html", {})


def targets(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "query":
        result1 = execute_sql_in_db("select http_domain from %s" % first_targets_table_name, db_name)
        RESULT1 = ""
        if len(result1) != 0:
            for each in result1:
                RESULT1 += each[0] + "\n"
        else:
            RESULT1 = "None\n"
        result2 = execute_sql_in_db("select http_domain from %s" % targets_table_name, db_name)
        RESULT2 = ""
        if len(result2) != 0:
            for each in result2:
                RESULT2 += each[0] + "\n"
        else:
            RESULT2 = "None\n"
        string = "first targets:\n" + RESULT1 + "\n" + "targets:\n" + RESULT2
        string = string.replace("\n", "<br>")
        return HttpResponse(string)
    elif action == "add":
        targetValue = get_http_domain_from_url(targetValue)
        execute_sql_in_db("insert into %s(http_domain,domain) values('%s','%s')" %
                          (targets_table_name, targetValue, targetValue.split("/")[-1]), db_name)
        string = "add new target %s for scan successully:D" % targetValue
        return HttpResponse(string)
    elif action == "delete":
        targetValue = get_http_domain_from_url(targetValue)
        execute_sql_in_db("DELETE FROM `%s` WHERE http_domain='%s'" %
                          (targets_table_name, targetValue), db_name)
        string = "delete target %s from db successully:D" % targetValue
        return HttpResponse(string)
    else:
        print("normal visit without action request to targets.html")
        pass

    # 下面这句不能少,下面这句是作为没有action[query/add/delete]查询时的正常情况下的显示页面的处理情况
    return render(request, "targets.html", {})


@login_required
def getPangSub(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "getPang":
        result = get_pang_domains(targetValue)
        return HttpResponse(result.replace("\n", "<br>"))
    elif action == "getSub":
        result = get_sub_domains(targetValue)
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("getPangSub.html", {})


@login_required
def xcdn(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    print(action)
    if targetValue != None:
        print(targetValue)
    if action == "xcdn":
        process = Xcdn(targetValue)
        result = process.return_value
        if result == 0:
            result = "Sorry,I tried,but failed."
        return HttpResponse(result)
    else:
        return render_to_response("xcdn.html", {})


@login_required
def highRisk(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "highRisk":
        result = single_risk_scan(targetValue)
        if result == "":
            result = "Sorry,no high risk vul."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("highRisk.html", {})


@login_required
def sqli(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "sqli":
        result = sqli_scan(targetValue)
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("sqli.html", {})


@login_required
def xdir(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "xdir":
        result = single_dirb_scan(targetValue)
        if result == "":
            result = "Sorry,no dir got."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("xdir.html", {})


@login_required
def xcms(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "xcms":
        result = single_cms_scan(targetValue)
        if result == "":
            result = "Sorry,got no cms vul."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("xcms.html", {})


@login_required
def xwebshell(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "xwebshell":
        result = crack_webshell(targetValue)
        if result == "":
            result = "Sorry,webshell not cracked."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("xwebshell.html", {})


@login_required
def xadmin(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "xadmin":
        result = crack_admin_login_url(targetValue)
        if result == "":
            result = "Sorry,admin login page not cracked."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("xadmin.html", {})


@login_required
def xwaf(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "xwaf":
        result = Xwaf(targetValue, False)
        result = result.returnValue
        if result == "":
            result = "Sorry,waf not bypassed."
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("xwaf.html", {})


@login_required
def dbquery(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "dbquery":
        result = execute_sql_in_db(targetValue, db_name)
        result = str(result)
        return HttpResponse(result.replace("\n", "<br>"))
    else:
        return render_to_response("dbquery.html", {})


@login_required
def result(request):
    targetValue = request.GET.get('targetValue')
    action = request.GET.get('action')
    if targetValue != None:
        print(targetValue)
    if action == "result" and targetValue == "initShowResult":
        firstTargets = execute_sql_in_db("select http_domain from %s" % first_targets_table_name, db_name)
        targets = execute_sql_in_db("select http_domain from %s" % targets_table_name, db_name)
        returnString = ""

        firstTargetsValue = "firstTargets,"
        targetsValue = "targets,"

        if len(firstTargets) == 0:
            pass
        else:
            for eachTarget in firstTargets:
                eachHttpDomain = eachTarget[0]
                firstTargetsValue += eachHttpDomain + ","
        firstTargetsValue = firstTargetsValue[:-1] + ";"
        if len(targets) == 0:
            pass
        else:
            for eachTarget in targets:
                eachHttpDomain = eachTarget[0]
                targetsValue += eachHttpDomain + ","
            targetsValue = targetsValue[:-1]

        # eg.返回为
        # firstTargets,http://www.baidu.com,http://www.nihao.com;targets,http://www.wohao.com,http://www.dajiahao.com
        returnString = firstTargetsValue + targetsValue

        print(returnString)
        return HttpResponse(returnString)

    elif action == "result" and targetValue != "initShowResult":
        # targetValue不为initShowResult时通过targetValue参数传递的内容是http_domain格式的目标,这种情况返回与该目
        # 标相关的所有扫描结果,(如果在扫描范围内)包括子域和旁站
        http_domain = targetValue
        print(http_domain)
        tableNameList = get_target_table_name_list(http_domain)
        # 下面的tableName是targets或first_targets
        tableName = tableNameList[0]

        #原来这里也显示urls和resource_files字段,后来决定不显示这两个字段
        resultColumns = ["risk_scan_info", "script_type", "dirb_info", "sqlis", "robots_and_sitemap", "cms_value", "cms_scan_info", "like_admin_login_urls",
                         "cracked_admin_login_urls_info", "like_webshell_urls", "cracked_webshell_urls_info",
                         "whois_info", "pang_domains", "sub_domains"]
        returnValue = ""
        for columnName in resultColumns:
            result = execute_sql_in_db("select %s from %s where http_domain='%s'" %
                                       (columnName, tableName, http_domain), db_name)
            if len(result[0][0]) == 0:
                columnNameResult = ""
            else:
                columnNameResult = "%s:\n&nbsp&nbsp&nbsp&nbsp" % columnName.replace(
                    "_", " ") + result[0][0] + "\n\n"
            returnValue += columnNameResult

        # 如果有旁站则加上旁站扫描结果
        targetPangTableName = http_domain.split("/")[-1].replace(".", "_") + "_pang"
        if exist_table_in_db(targetPangTableName, db_name) == True:
            pangDoamins = execute_sql_in_db("select http_domain from %s" % targetPangTableName, db_name)
            pangDoaminsList = []
            for each in pangDoamins:
                pangDoaminsList.append(each[0])

            # 下面加上旁站扫描结果
            returnValue += "下面是旁站扫描结果:\n\n"
            for eachPangDomain in pangDoaminsList:
                for columnName in resultColumns:
                    if columnName not in ["pang_domains", "sub_domains"]:
                        result = execute_sql_in_db("select %s from %s where http_domain='%s'" %
                                                   (columnName, targetPangTableName, eachPangDomain), db_name)
                        if len(result[0][0]) == 0:
                            columnNameResult = ""
                        else:
                            columnNameResult = "%s:\n&nbsp&nbsp&nbsp&nbsp" % columnName.replace(
                                "_", " ") + result[0][0] + "\n\n"
                        returnValue += columnNameResult

        # 如果有子站则加上子站扫描结果
        targetSubTableName = http_domain.split("/")[-1].replace(".", "_") + "_sub"
        if exist_table_in_db(targetSubTableName, db_name) == True:
            SubDoamins = execute_sql_in_db("select http_domain from %s" % targetSubTableName, db_name)
            SubDoaminsList = []
            for each in SubDoamins:
                SubDoaminsList.append(each[0])

            # 下面加上子站扫描结果
            returnValue += "下面是子站扫描结果:\n\n"
            for eachSubDomain in SubDoaminsList:
                for columnName in resultColumns:
                    if columnName not in ["pang_domains", "sub_domains"]:
                        result = execute_sql_in_db("select %s from %s where http_domain='%s'" %
                                                   (columnName, targetSubTableName, eachSubDomain), db_name)
                        if len(result[0][0]) == 0:
                            columnNameResult = ""
                        else:
                            columnNameResult = "%s:\n&nbsp&nbsp&nbsp&nbsp" % columnName.replace(
                                "_", " ") + result[0][0] + "\n\n"
                        returnValue += columnNameResult

        if returnValue == "":
            returnValue += "there is no result about %s" % http_domain
        return HttpResponse(returnValue.replace("\n", "<br>"))

    else:
        return render_to_response("result.html", {})
