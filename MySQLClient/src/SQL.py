# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2023 Komorebi660 All rights reserved.
# ----------------------------------------------------------
book_gen = "DROP TABLE IF EXISTS Borrow;\
            DROP TABLE IF EXISTS Book;\
            CREATE TABLE Book (\
                ID CHAR(8),\
                _name VARCHAR(10) NOT NULL,\
                author VARCHAR(10),\
                price FLOAT,\
                _status INT DEFAULT 0,\
                CONSTRAINT PKb PRIMARY KEY (ID),\
                CONSTRAINT Cons CHECK (_status IN (0 , 1))\
            );\
            insert into Book value('b1', '数据库系统实现', 'Ullman', 59.0, 0);\
            insert into Book value('b2', '数据库系统概念', 'Abraham', 59.0, 1);\
            insert into Book value('b3', 'C++ Primer', 'Stanley', 78.6, 1);\
            insert into Book value('b4', 'Redis设计与实现', '黄建宏', 79.0, 1);\
            insert into Book value('b5', '人类简史', 'Yuval', 68.00, 0);\
            insert into Book value('b6', '史记(公版)', '司马迁', 220.2, 1);\
            insert into Book value('b7', 'Oracle编程艺术', 'Thomas', 43.1, 1);\
            insert into Book value('b8', '分布式系统及其应用', '邵佩英', 30.0, 0);\
            insert into Book value('b9', 'Oracle管理', '张立杰', 51.9, 1);\
            insert into Book value('b10', '数理逻辑', '汪芳庭', 22.0, 0);\
            insert into Book value('b11', '三体', '刘慈欣', 23.0, 0);\
            insert into Book value('b12', 'Fun python', 'Luciano', 354.2, 0);\
            insert into Book value('b13', 'Learn SQL', 'Seyed', 23.0, 1);\
            insert into Book value('b14', 'Perl&MySQL', '徐泽平', 23.0, 1);"

reader_gen = "DROP TABLE IF EXISTS Borrow;\
            DROP TABLE IF EXISTS Reader;\
            CREATE TABLE Reader (\
                ID CHAR(8),\
                _name VARCHAR(10) NOT NULL,\
                age INT,\
                address VARCHAR(20),\
                CONSTRAINT PKr PRIMARY KEY (ID)\
            );\
            insert into Reader value('r1', '李林', 18, '中国科学技术大学东校区');\
            insert into Reader value('r2', 'Rose', 22, '中国科学技术大学北校区');\
            insert into Reader value('r3', '罗永平', 23, '中国科学技术大学西校区');\
            insert into Reader value('r4', 'Nora', 26, '中国科学技术大学北校区');\
            insert into Reader value('r5', '汤晨', 22, '先进科学技术研究院');\
            insert into Reader value('r6', '李小一', 18, '中国科学技术大学东校区');\
            insert into Reader value('r7', '王二', 22, '中国科学技术大学北校区');\
            insert into Reader value('r8', '赵三', 23, '中国科学技术大学西校区');\
            insert into Reader value('r9', '魏四', 26, '中国科学技术大学北校区');\
            insert into Reader value('r10', '汤大晨', 22, '先进科学技术研究院');\
            insert into Reader value('r11', '李平', 18, '中国科学技术大学东校区');\
            insert into Reader value('r12', 'Lee', 22, '中国科学技术大学北校区');\
            insert into Reader value('r13', 'Jack', 23, '中国科学技术大学西校区');\
            insert into Reader value('r14', 'Bob', 26, '中国科学技术大学北校区');\
            insert into Reader value('r15', '李晓', 22, '先进科学技术研究院');\
            insert into Reader value('r16', '王林', 18, '中国科学技术大学东校区');\
            insert into Reader value('r17', 'Mike', 22, '中国科学技术大学北校区');\
            insert into Reader value('r18', '范维', 23, '中国科学技术大学西校区');\
            insert into Reader value('r19', 'David', 26, '中国科学技术大学北校区');\
            insert into Reader value('r20', 'Vipin', 22, '先进科学技术研究院');\
            insert into Reader value('r21', '林立', 18, '中国科学技术大学东校区');\
            insert into Reader value('r22', '张悟', 22, '中国科学技术大学北校区');\
            insert into Reader value('r23', '袁平', 23, '中国科学技术大学西校区');"

borrow_gen = "DROP TABLE IF EXISTS Borrow;\
            CREATE TABLE Borrow (\
                book_ID CHAR(8),\
                reader_ID CHAR(8),\
                borrow_date DATE,\
                return_date DATE,\
                CONSTRAINT PKborrow PRIMARY KEY (book_ID , reader_ID),\
                FOREIGN KEY (book_ID)\
                    REFERENCES Book (ID),\
                FOREIGN KEY (reader_ID)\
                    REFERENCES Reader (ID)\
            );\
            insert into Borrow value('b5','r1',  '2021-03-12', '2021-04-07');\
            insert into Borrow value('b6','r1',  '2021-03-08', '2021-03-19');\
            insert into Borrow value('b11','r1',  '2021-01-12', '2021-05-19');\
            insert into Borrow value('b3', 'r2', '2021-02-22', '2021-03-10');\
            insert into Borrow value('b9', 'r2', '2021-02-22', '2021-04-10');\
            insert into Borrow value('b7', 'r2', '2021-04-11', NULL);\
            insert into Borrow value('b1', 'r3', '2021-04-02', '2021-07-19');\
            insert into Borrow value('b2', 'r3', '2021-04-02', '2021-07-19');\
            insert into Borrow value('b4', 'r3', '2021-04-02', '2021-04-09');\
            insert into Borrow value('b7', 'r3', '2021-04-02', '2021-04-09');\
            insert into Borrow value('b6', 'r4', '2021-03-31', NULL);\
            insert into Borrow value('b12', 'r4', '2021-03-31', '2021-07-19');\
            insert into Borrow value('b4', 'r5', '2021-04-10', NULL);\
            insert into Borrow value('b11','r5',  '2021-08-12', '2021-09-19');\
            insert into Borrow value('b3', 'r6', '2021-04-10', '2022-01-01');\
            insert into Borrow value('b1', 'r7', '2021-08-10', '2021-12-19');\
            insert into Borrow value('b1', 'r8', '2022-01-10', '2022-02-19');\
            insert into Borrow value('b5','r8',  '2021-07-12', '2021-10-07');\
            insert into Borrow value('b1', 'r9', '2022-03-10', '2022-03-19');\
            insert into Borrow value('b2', 'r9', '2022-03-10', '2021-03-19');\
            insert into Borrow value('b2', 'r10', '2022-03-20', NULL);\
            insert into Borrow value('b5','r10',  '2021-05-12', '2021-06-07');\
            insert into Borrow value('b11','r10',  '2021-10-12', '2021-11-19');\
            insert into Borrow value('b3', 'r12', '2021-04-10', '2021-08-19');\
            insert into Borrow value('b3', 'r13', '2021-09-10', '2021-12-19');\
            insert into Borrow value('b3', 'r14', '2022-01-10', NULL);\
            insert into Borrow value('b9', 'r15', '2021-04-19', '2021-08-19');\
            insert into Borrow value('b9', 'r16', '2021-10-10', '2021-12-19');\
            insert into Borrow value('b9', 'r17', '2022-01-10', NULL);\
            insert into Borrow value('b11','r17',  '2021-12-12', '2022-01-19');\
            insert into Borrow value('b12', 'r18', '2021-10-10', '2021-12-19');\
            insert into Borrow value('b13', 'r18', '2021-10-10', '2021-12-19');\
            insert into Borrow value('b13', 'r19', '2022-01-10', NULL);\
            insert into Borrow value('b5','r19',  '2022-01-12', '2022-03-07');\
            insert into Borrow value('b8', 'r20', '2022-01-10', '2022-02-19');\
            insert into Borrow value('b14', 'r22', '2021-10-10', '2021-12-19');\
            insert into Borrow value('b14', 'r23', '2022-01-10', NULL);"

table_del = "DROP TABLE IF EXISTS Borrow;\
            DROP TABLE IF EXISTS Book;\
            DROP TABLE IF EXISTS Reader;"
