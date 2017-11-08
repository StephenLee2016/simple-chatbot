# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

import os, sys
import aiml


def add_rules():
    rule_path = os.getcwd()
    mybot = aiml.Kernel()

    # 加载aiml规则模板
    mybot.learn(rule_path + '/matcher/rules/Common_conversation.aiml')
    mybot.learn(rule_path + '/matcher/rules/bye.aiml')
    #mybot.learn(rule_path + '/matcher/rules/tools.aiml')
    #mybot.learn(rule_path + '/matcher/rules/bad.aiml')
    #mybot.learn(rule_path + '/matcher/rules/funny.aiml')
    #mybot.learn(rule_path + '/matcher/rules/OrdinaryQuestion.aiml')

    #mybot.learn(rule_path + '/matcher/rules/persionname.aiml')

    return mybot

def get_rules():
    mybot = add_rules()
    return mybot