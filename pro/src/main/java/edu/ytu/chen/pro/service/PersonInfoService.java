package edu.ytu.chen.pro.service;

public interface PersonInfoService {

    /**
     * 根据学号获取标签
     * @param stuNum 学号
     * @return
     */
    String getLabels(String stuNum);

    /**
     * 根据学号获取提交总量
     * @param stuNum 学号
     * @return
     */
    String getSubmitData(String stuNum);

    /**
     * 根据学号获取AC总量
     * @param stuNum 学号
     * @return
     */
    String getAcceptData(String stuNum);
}
