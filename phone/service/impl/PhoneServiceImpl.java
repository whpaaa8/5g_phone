package com.phone.service.impl;

import com.phone.dao.PhoneDao;
import com.phone.pojo.Phone;
import com.phone.service.PhoneService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PhoneServiceImpl implements PhoneService {

    @Autowired
    private PhoneDao phoneDao;
    @Override
    public boolean save(Phone phone) {
        int result = phoneDao.save(phone);
        return result > 0;
    }

    @Override
    public boolean delete(String goods_id) {
        int result = phoneDao.delete(goods_id);
        return result > 0;
    }

    @Override
    public List<Phone> getByBrand(String brand) {
        List<Phone> phones = phoneDao.getByBrand(brand);
        return phones;
    }

    @Override
    public List<Phone> getAll() {
        return phoneDao.getAll();
    }

    @Override
    public int getCount() {
        return phoneDao.getCount();
    }

    @Override
    public Boolean isExist(String goods_id) {
        return phoneDao.exist(goods_id) == 1;
    }
}
