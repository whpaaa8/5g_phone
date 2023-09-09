package com.phone.service;

import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;

@Transactional
public interface UpdateService {

    /**
     * 更新信息
     * @return
     */
    public int Update() throws IOException;

    public Boolean UpdateById(String id) throws  IOException;
}
