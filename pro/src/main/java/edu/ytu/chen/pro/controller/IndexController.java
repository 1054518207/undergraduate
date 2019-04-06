package edu.ytu.chen.pro.controller;

import edu.ytu.chen.pro.service.PythonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;

@Controller
public class IndexController {

    @Autowired
    private PythonService pythonService;

    @RequestMapping(value = {"", "index"}, method = RequestMethod.GET)
    public String getIndex(@RequestParam(required = false) HttpServletRequest httpServletRequest, Model model){
        return "index";
    }

    public String getPythonInfo(){
        String content = pythonService.getPythonInfo();
        /*if(content == null || content == ""){
            model.addAttribute("msg", "error");
            return "index";
        }else {
            model.addAttribute("msg",content);
            System.out.println(content);
            return "index";
        }*/
        return content;
    }
}
