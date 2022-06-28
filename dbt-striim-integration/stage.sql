with test as (

    select
        *
    from {{ source('retailcdc', 'retailazure') }}

)

select * from test
