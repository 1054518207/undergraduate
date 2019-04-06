package edu.ytu.chen.pro.service.impl;

import edu.ytu.chen.pro.service.PythonService;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;

@Service
public class PythonServiceImpl implements PythonService {



    @Override
    public String getPythonInfo() {
        String con = "";
        ProcessBuilder pb = new ProcessBuilder(
                new String[]{
                        "python",
                        "D:/undergraduate/python crawl/chen/testDataFrame.py"
                }
        );
        pb.redirectErrorStream(true);
        try {
            Process p = pb.start();
            InputStream is = p.getInputStream();
            int in = -1;
            while ((in = is.read()) != -1) {
                con += (char)in;
                //System.out.print((char)in);
            }
            int exitWith = p.exitValue();
            //System.out.println("\nExited with " + exitWith);
        } catch (IOException exp) {
            exp.printStackTrace();
        }
        return con;
    }
}
