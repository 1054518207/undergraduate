package edu.ytu.chen.pro.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class PersonInfoController {

    @RequestMapping(value = "personinfo", method = RequestMethod.GET)
    public String getPersonInfo(){
        return "personinfo";
    }



}
