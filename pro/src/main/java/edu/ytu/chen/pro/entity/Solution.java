package edu.ytu.chen.pro.entity;

import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;

@Table(name = "jol.solution")
public class Solution {
    @Id
    @Column(name = "solution_id")
    private Integer solutionId;

    @Column(name = "problem_id")
    private Integer problemId;

    @Column(name = "user_id")
    private String userId;

    private Integer time;

    private Integer memory;

    @Column(name = "in_date")
    private Date inDate;

    private Short result;

    private Integer language;

    private String ip;

    @Column(name = "contest_id")
    private Integer contestId;

    private Byte valid;

    private Byte num;

    @Column(name = "code_length")
    private Integer codeLength;

    private Date judgetime;

    @Column(name = "pass_rate")
    private BigDecimal passRate;

    @Column(name = "lint_error")
    private Integer lintError;

    private String judger;

    /**
     * @return solution_id
     */
    public Integer getSolutionId() {
        return solutionId;
    }

    /**
     * @param solutionId
     */
    public void setSolutionId(Integer solutionId) {
        this.solutionId = solutionId;
    }

    /**
     * @return problem_id
     */
    public Integer getProblemId() {
        return problemId;
    }

    /**
     * @param problemId
     */
    public void setProblemId(Integer problemId) {
        this.problemId = problemId;
    }

    /**
     * @return user_id
     */
    public String getUserId() {
        return userId;
    }

    /**
     * @param userId
     */
    public void setUserId(String userId) {
        this.userId = userId;
    }

    /**
     * @return time
     */
    public Integer getTime() {
        return time;
    }

    /**
     * @param time
     */
    public void setTime(Integer time) {
        this.time = time;
    }

    /**
     * @return memory
     */
    public Integer getMemory() {
        return memory;
    }

    /**
     * @param memory
     */
    public void setMemory(Integer memory) {
        this.memory = memory;
    }

    /**
     * @return in_date
     */
    public Date getInDate() {
        return inDate;
    }

    /**
     * @param inDate
     */
    public void setInDate(Date inDate) {
        this.inDate = inDate;
    }

    /**
     * @return result
     */
    public Short getResult() {
        return result;
    }

    /**
     * @param result
     */
    public void setResult(Short result) {
        this.result = result;
    }

    /**
     * @return language
     */
    public Integer getLanguage() {
        return language;
    }

    /**
     * @param language
     */
    public void setLanguage(Integer language) {
        this.language = language;
    }

    /**
     * @return ip
     */
    public String getIp() {
        return ip;
    }

    /**
     * @param ip
     */
    public void setIp(String ip) {
        this.ip = ip;
    }

    /**
     * @return contest_id
     */
    public Integer getContestId() {
        return contestId;
    }

    /**
     * @param contestId
     */
    public void setContestId(Integer contestId) {
        this.contestId = contestId;
    }

    /**
     * @return valid
     */
    public Byte getValid() {
        return valid;
    }

    /**
     * @param valid
     */
    public void setValid(Byte valid) {
        this.valid = valid;
    }

    /**
     * @return num
     */
    public Byte getNum() {
        return num;
    }

    /**
     * @param num
     */
    public void setNum(Byte num) {
        this.num = num;
    }

    /**
     * @return code_length
     */
    public Integer getCodeLength() {
        return codeLength;
    }

    /**
     * @param codeLength
     */
    public void setCodeLength(Integer codeLength) {
        this.codeLength = codeLength;
    }

    /**
     * @return judgetime
     */
    public Date getJudgetime() {
        return judgetime;
    }

    /**
     * @param judgetime
     */
    public void setJudgetime(Date judgetime) {
        this.judgetime = judgetime;
    }

    /**
     * @return pass_rate
     */
    public BigDecimal getPassRate() {
        return passRate;
    }

    /**
     * @param passRate
     */
    public void setPassRate(BigDecimal passRate) {
        this.passRate = passRate;
    }

    /**
     * @return lint_error
     */
    public Integer getLintError() {
        return lintError;
    }

    /**
     * @param lintError
     */
    public void setLintError(Integer lintError) {
        this.lintError = lintError;
    }

    /**
     * @return judger
     */
    public String getJudger() {
        return judger;
    }

    /**
     * @param judger
     */
    public void setJudger(String judger) {
        this.judger = judger;
    }
}