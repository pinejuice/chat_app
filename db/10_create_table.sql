CREATE TABLE user_tbl (
    user_id varchar(20) NOT NULL primary key,
    nick_name varchar(20) NOT NULL,
    login_pw text NOT NULL,
    icon text
);

CREATE TABLE chat_tbl (
    chat_id bigint NOT NULL primary key DEFAULT nextval('chat_seq'),
    post_content text NOT NULL,
    post_user_id varchar(20) NOT NULL,
    post_timestamp timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
